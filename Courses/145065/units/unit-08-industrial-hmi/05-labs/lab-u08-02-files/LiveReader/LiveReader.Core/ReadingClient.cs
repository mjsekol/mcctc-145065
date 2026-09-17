// ReadingClient.cs  .  Lab U08-02  .  STARTER
//
// The one class that talks to the Line 3 sensor service. You write PollAsync.
//
// What PollAsync must do, in order (the lab's steps 3 to 8):
//
//   1. GET the readings address, and AWAIT it. Never .Result, never .Wait().
//   2. Give up after Timeout, and say Timeout.
//   3. Anything but 200 is HttpError.
//   4. Read the body and hand it to ReadingParser.Parse. A parse that fails
//      is MalformedReply.
//   5. A connection that fails is ServiceDown.
//   6. If the CALLER cancels, let the OperationCanceledException go. That is
//      not a timeout.
//
// It must never throw for a network problem, and never return an old value.
//
// The service is Riverside Fabrication's Line 3 sensor service. Riverside
// Fabrication is a composite, invented for this course. This class only ever
// sends GET. It never asks the service to change anything.

using System.Net;
using System.Net.Http;

namespace Line3.Hmi.Core;

public sealed class ReadingClient : IDisposable
{
    public const string ReadingsPath = "api/readings";

    // The contract reply is a few hundred bytes. Anything far larger is not the
    // contract. HttpClient refuses to buffer more than this, so a broken or
    // hostile device cannot fill the panel's memory. That is bounds checking.
    public const int MaxReplyBytes = 64 * 1024;

    private readonly HttpClient http;

    public ReadingClient(Uri serviceUrl, TimeSpan timeout)
    {
        if (timeout <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(timeout), "timeout must be positive");
        }

        Timeout = timeout;

        // "http://127.0.0.1:8700" and "http://127.0.0.1:8700/" both become
        // "http://127.0.0.1:8700/api/readings".
        string root = serviceUrl.ToString().EndsWith('/') ? serviceUrl.ToString() : serviceUrl + "/";
        ReadingsUrl = new Uri(new Uri(root), ReadingsPath);

        // ONE HttpClient for the life of this object, not one per poll. Its own
        // timeout is switched off, because PollAsync applies Timeout itself and
        // needs to tell "we gave up" apart from "the caller cancelled".
        http = new HttpClient
        {
            Timeout = System.Threading.Timeout.InfiniteTimeSpan,
            MaxResponseContentBufferSize = MaxReplyBytes,
        };
    }

    public TimeSpan Timeout { get; }

    public Uri ReadingsUrl { get; }

    /// <summary>Ask the service once. Completes within about <see cref="Timeout"/>.</summary>
    public Task<PollResult> PollAsync(CancellationToken cancel = default)
    {
        // TODO steps 3 to 8. Delete this line when you start. Add the async
        // keyword to this method's signature when you write your first await.
        throw new NotImplementedException("PollAsync is not written yet. Start at step 3.");
    }

    private static PollResult Failed(PollFailure failure, string detail) =>
        PollResult.Failed(failure, detail, DateTimeOffset.UtcNow);

    public void Dispose() => http.Dispose();
}
