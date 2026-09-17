using System.Net.Http;

namespace Line3.Reader;

/// <summary>
/// Reads the Line 3 sensor service over HTTP. One HttpClient is reused for the
/// life of the source, which avoids exhausting sockets.
/// </summary>
public sealed class HttpReadingSource : IReadingSource, IDisposable
{
    private readonly HttpClient http = new();
    private readonly Uri readingsUrl;

    public HttpReadingSource(LimitsFile limits)
    {
        readingsUrl = new Uri(limits.ServiceUrl, "api/readings");
        Timeout = limits.RequestTimeout;
    }

    /// <inheritdoc />
    public TimeSpan Timeout { get; }

    /// <inheritdoc />
    public async Task<ReadResult> ReadAsync(CancellationToken cancel = default)
    {
        try
        {
            using HttpResponseMessage response = await http.GetAsync(readingsUrl, cancel);
            if (!response.IsSuccessStatusCode)
            {
                return ReadResult.Failed($"the service answered {(int)response.StatusCode}");
            }

            string body = await response.Content.ReadAsStringAsync(cancel);
            ReadingBatch? batch = ReadingParser.Parse(body, out string? problem);
            return batch is null ? ReadResult.Failed(problem!) : ReadResult.Success(batch);
        }
        catch (HttpRequestException ex)
        {
            return ReadResult.Failed("the connection failed: " + ex.Message);
        }
        catch (TaskCanceledException) when (!cancel.IsCancellationRequested)
        {
            // The request ran past the timeout.
            return ReadResult.Failed($"no answer within {Timeout.TotalSeconds:0.0} s");
        }
    }

    public void Dispose() => http.Dispose();
}
