# Daylight Saving Time (DST): Clock and Prayer-Time Issues

Draft for factual review. Not included in the published help-center catalog yet.

## Identify what is one hour off

After a daylight saving time change, first compare the TV's current clock, the timings saved in the Masjidal portal, and the timetable approved by your masjid. A device-clock problem and a prayer-timetable problem need different checks.

| What you notice | What to check first |
|---|---|
| The TV's current clock is one hour ahead or behind | Device date/time, time zone, internet connection, and time synchronization |
| The current clock is correct, but Salah times are wrong | The masjid's location and the calculated or uploaded Salah timetable |
| Salah times are correct, but Iqamah times need to change | Your masjid's saved Iqamah entries and their effective dates |
| One TV is wrong but other screens are correct | Compare the affected player's clock and app with a working screen |

## If the signage player's clock is wrong

1. Check the current local time against a reliable clock and confirm that your location observes DST.
2. Check whether other screens using the same masjid account have the same problem.
3. Confirm the affected player is connected to the internet.
4. Follow the existing [Current Time Sync (Signage Player)](../article/index.html?topic=time-sync) guide if its clock is out of sync. That guide describes installing and configuring the NTP app on the Masjidal Signage Player.

An NTP/time-sync check addresses an out-of-sync device clock. It does not establish that an incorrect time-zone or DST configuration has been corrected. The exact supported device time-zone/DST procedure needs confirmation before this draft is published.

## If the clock is correct but Salah times are wrong

1. In the portal, open Timings > Salah Timings.
2. Compare the displayed dates and times with your masjid's approved timetable.
3. Identify whether you use calculated times or upload your own timetable.
4. Follow [Salah (Athan)](../article/index.html?topic=salah) to review the existing calculation settings or uploaded timings. Saving changes to calculation methods or offsets regenerates and overrides existing timings; review your current setup before doing so.

Do not apply a blanket one-hour offset as a substitute for diagnosing the clock, time zone, or timetable problem.

## If only Iqamah times need to change

Iqamah entries describe the congregation times chosen by your masjid. In Timings > Iqamah Timings, check the entry whose effective date covers the DST change. The published guide explains that each entry remains in effect until the next saved change date. Follow [Iqamah](../article/index.html?topic=iqamah) to add or edit the intended change.

## Information to send support

Include your masjid name and location, device type, date of the issue, a photo of the displayed clock and timings, the expected times, and whether the portal and other screens show the same issue. Contact masjidsupport@masjidal.com.

## Questions needed to finish

- Should this article cover signage-player clocks, incorrect prayer times, or both? Does it also cover Athan Frame/Clock or phone-app issues?
- What is the confirmed portal/device path and field name for the time-zone or DST fix? Is there a DST toggle, an automatic time-zone option, or a support-side correction?
- Is a restart or refresh needed after applying that correction?

## Research notes

- Public portal entry: https://portal.masjidal.com/ (requires sign-in; no account used).
- https://help.masjidal.com/knowledge-base/time-sync/ documents NTP clock synchronization, without a DST-specific fix.
- https://help.masjidal.com/knowledge-base/salah/ documents calculated/uploaded timings and warns that saving calculation settings overrides existing timings.
- https://help.masjidal.com/knowledge-base/iqamah/ documents effective-date-based Iqamah changes.
- https://help.masjidal.com/aframe/help documents separate Athan Frame standalone/synced modes. Those controls should not be presented as signage-player settings.
- Public portal JavaScript inspected for daylight-saving terminology. It did not establish a supported DST troubleshooting procedure.
