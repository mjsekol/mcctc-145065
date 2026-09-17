// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/Contract.cs.
// Given to you. Read it; you do not need to change it.
//
// Contract.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// The shape of one reply from the Line 3 sensor service. The Python side of
// this contract is sensor-service/readings.py. If one changes, both change.
//
//   GET /api/readings -> 200
//   {
//     "device": "line3-pi",
//     "sequence": 1042,
//     "sampled_at": "2027-01-11T14:03:22Z",
//     "sensors": [
//       {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
//       ...
//     ]
//   }
//
// Setting: Riverside Fabrication, Line 3, is a composite. It is not a real shop.

namespace Line3.Hmi.Core;

/// <summary>
/// One sensor in one reply. <see cref="Value"/> is null exactly when
/// <see cref="Ok"/> is false. The parser guarantees that, so no other code
/// has to check both.
/// </summary>
public sealed record SensorSample(string Id, string Kind, double? Value, string Unit, bool Ok)
{
    /// <summary>Why the parser marked this sensor not ok, when the reply itself did not.</summary>
    public string? ContractProblem { get; init; }
}

/// <summary>One whole reply: which device, which sample, when, and every sensor.</summary>
public sealed record ReadingSnapshot(
    string Device,
    long Sequence,
    DateTimeOffset SampledAt,
    IReadOnlyList<SensorSample> Sensors)
{
    public SensorSample? Find(string sensorId) =>
        Sensors.FirstOrDefault(s => string.Equals(s.Id, sensorId, StringComparison.Ordinal));
}
