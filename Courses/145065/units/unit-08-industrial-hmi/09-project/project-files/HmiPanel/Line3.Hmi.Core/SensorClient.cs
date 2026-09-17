// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/SensorClient.cs.
// Given to you. Read it; you do not need to change it.
//
// SensorClient.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// The only class in the panel that talks to the network. One GET per poll,
// with a hard timeout, and every way it can go wrong turned into a
// PollFailure. It never throws for a network problem and never returns an
// old value as if it were new.
//
// WHY THIS NEVER BLOCKS THE UI THREAD. PollAsync awaits HttpClient all the
// way down. While it waits, the thread that called it is free, so the window
// keeps repainting and the buttons keep working. The version that freezes the
// window calls .Result or .Wait() on the task. There is none of that here, and
// a test proves PollAsync hands back control before the service answers.
//
// Four failures, because an operator or a technician fixes each differently:
//
//   ServiceDown     nothing is listening. The Pi is off, unplugged, or the
//                   service is not running.
//   Timeout         something is listening and did not answer in time.
//   HttpError       it answered with a status other than 200.
//   MalformedReply  it answered 200 with something that is not the contract.

using System.Net;
using System.Net.Http;
using System.Net.Sockets;
using System.Text;

namespace Line3.Hmi.Core;

public enum PollFailure
{
    None,
    ServiceDown,
    Timeout,
    HttpError,
    MalformedReply,
}

/// <summary>The outcome of one poll. Snapshot is set exactly when Failure is None.</summary>
public sealed record PollResult(ReadingSnapshot? Snapshot, PollFailure Failure, string Detail, DateTimeOffset ReceivedAt)
{
    public bool Ok => Failure == PollFailure.None;

    public static PollResult Success(ReadingSnapshot snapshot, DateTimeOffset at) =>
        new(snapshot, PollFailure.None, string.Empty, at);

    public static PollResult Failed(PollFailure failure, string detail, DateTimeOffset at) =>
        new(null, failure, detail, at);
}

public sealed class SensorClient : IDisposable
{
    public const string ReadingsPath = "api/readings";

    // The contract reply is a few hundred bytes. Anything far larger is not the
    // contract, and reading it all would waste the poll.
    public const int MaxReplyBytes = 64 * 1024;

    private readonly HttpClient http;
    private readonly IClock clock;
    private readonly Uri readingsUrl;

    public SensorClient(Uri serviceUrl, TimeSpan timeout, IClock clock, HttpMessageHandler? handler = null)
    {
        if (timeout <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(timeout), "timeout must be positive");
        }

        Timeout = timeout;
        this.clock = clock;
        string root = serviceUrl.ToString().EndsWith('/') ? serviceUrl.ToString() : serviceUrl + "/";
        readingsUrl = new Uri(new Uri(root), ReadingsPath);

        // HttpClient's own Timeout is switched off. This class applies its own,
        // so it can tell "we gave up" apart from "the caller cancelled".
        http = handler is null ? new HttpClient() : new HttpClient(handler, disposeHandler: false);
        http.Timeout = System.Threading.Timeout.InfiniteTimeSpan;
        http.MaxResponseContentBufferSize = MaxReplyBytes;
    }

    public TimeSpan Timeout { get; }

    public Uri ReadingsUrl => readingsUrl;

    /// <summary>
    /// Ask once. Always completes within about <see cref="Timeout"/>. Throws
    /// only OperationCanceledException, and only when <paramref name="cancel"/>
    /// was cancelled by the caller.
    /// </summary>
    public async Task<PollResult> PollAsync(CancellationToken cancel = default)
    {
        using CancellationTokenSource limit = CancellationTokenSource.CreateLinkedTokenSource(cancel);
        limit.CancelAfter(Timeout);

        try
        {
            using HttpRequestMessage request = new(HttpMethod.Get, readingsUrl);
            request.Headers.CacheControl = new System.Net.Http.Headers.CacheControlHeaderValue { NoStore = true };

            using HttpResponseMessage response = await http
                .SendAsync(request, HttpCompletionOption.ResponseHeadersRead, limit.Token)
                .ConfigureAwait(false);

            if (response.StatusCode != HttpStatusCode.OK)
            {
                return Fail(PollFailure.HttpError, $"the service answered {(int)response.StatusCode} {response.ReasonPhrase}");
            }

            string body = await ReadLimitedAsync(response.Content, limit.Token).ConfigureAwait(false);
            ParseResult parsed = ReadingParser.Parse(body);
            return parsed.Ok
                ? PollResult.Success(parsed.Snapshot!, clock.UtcNow)
                : Fail(PollFailure.MalformedReply, parsed.Error!);
        }
        catch (OperationCanceledException) when (cancel.IsCancellationRequested)
        {
            throw;
        }
        catch (OperationCanceledException)
        {
            return Fail(PollFailure.Timeout, $"no answer within {Timeout.TotalSeconds:0.0} s");
        }
        catch (HttpRequestException problem) when (IsNothingListening(problem))
        {
            return Fail(PollFailure.ServiceDown, "nothing is answering at " + readingsUrl.GetLeftPart(UriPartial.Authority));
        }
        catch (HttpRequestException problem)
        {
            // Connection reset, closed mid-reply, or a reply larger than the limit.
            return Fail(PollFailure.ServiceDown, "the connection failed: " + problem.Message);
        }
        catch (ReplyTooLargeException)
        {
            return Fail(PollFailure.MalformedReply, $"the reply was larger than {MaxReplyBytes} bytes");
        }
        catch (IOException problem)
        {
            return Fail(PollFailure.ServiceDown, "the connection failed: " + problem.Message);
        }
    }

    private PollResult Fail(PollFailure failure, string detail) => PollResult.Failed(failure, detail, clock.UtcNow);

    private static bool IsNothingListening(HttpRequestException problem) =>
        problem.InnerException is SocketException socket
        && socket.SocketErrorCode is SocketError.ConnectionRefused or SocketError.HostUnreachable
            or SocketError.NetworkUnreachable or SocketError.HostNotFound;

    private static async Task<string> ReadLimitedAsync(HttpContent content, CancellationToken cancel)
    {
        if (content.Headers.ContentLength is long declared && declared > MaxReplyBytes)
        {
            throw new ReplyTooLargeException();
        }

        await using Stream stream = await content.ReadAsStreamAsync(cancel).ConfigureAwait(false);
        using MemoryStream buffer = new();
        byte[] chunk = new byte[4096];
        int read;
        while ((read = await stream.ReadAsync(chunk, cancel).ConfigureAwait(false)) > 0)
        {
            if (buffer.Length + read > MaxReplyBytes)
            {
                throw new ReplyTooLargeException();
            }

            buffer.Write(chunk, 0, read);
        }

        return Encoding.UTF8.GetString(buffer.GetBuffer(), 0, (int)buffer.Length);
    }

    public void Dispose() => http.Dispose();

    private sealed class ReplyTooLargeException : Exception
    {
    }
}
