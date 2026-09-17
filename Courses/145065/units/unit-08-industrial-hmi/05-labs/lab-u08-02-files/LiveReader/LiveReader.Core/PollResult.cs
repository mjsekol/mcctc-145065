// PollResult.cs  .  Lab U08-02  .  given to you
//
// The outcome of one poll. Copied from the HMI anchor's SensorClient.cs, so
// the panel project in Weeks 15-16 uses the same names you use here.
//
// Four failures, because an operator or a technician fixes each differently:
//
//   ServiceDown     nothing answered: the Pi is off, unplugged, or the
//                   service is not running, or the connection broke
//   Timeout         something is listening and did not answer in time
//   HttpError       it answered with a status other than 200
//   MalformedReply  it answered 200 with something that is not the contract

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
