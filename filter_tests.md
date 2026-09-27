# Network Traffic Filtering — Rules and Test Evidence

## Environment

Testing was carried out on a personal Windows 11 laptop, since no dedicated Linux lab
environment was available. Windows Defender Firewall (via PowerShell's `NetFirewallRule`
cmdlets) was used in place of `iptables`/`ufw`, as it provides equivalent inbound
allow/block filtering functionality.

The "server" was simulated using Python's built-in HTTP server (`python -m http.server 5000`)
running from the project folder, representing the student records service. The laptop hosted
its own Windows Mobile Hotspot (IP `192.168.137.1`) so that a second physical device (an iPhone,
IP `192.168.137.24`) could connect as a genuinely separate host — this was necessary because
the original mobile hotspot network had client (AP) isolation enabled, which silently blocks
device-to-device traffic regardless of firewall rules; hosting the hotspot from the laptop
itself removed that restriction.

## Firewall Rules Applied (PowerShell / Windows Defender Firewall)

```powershell
$serverPort = 5000
$staffIP = "192.168.137.24"   # phone, representing an authorised staff device

# a & c: block all inbound traffic to the service by default
New-NetFirewallRule -DisplayName "Block-Others-5000" -Direction Inbound -Protocol TCP -LocalPort $serverPort -RemoteAddress Any -Action Block

# b: permit the specific authorised staff IP to the service
New-NetFirewallRule -DisplayName "Allow-Staff-5000" -Direction Inbound -Protocol TCP -LocalPort $serverPort -RemoteAddress $staffIP -Action Allow
```

Full command output (rule IDs, properties) is included in `evidence/firewall_rules_output.txt`.

### Note on rule precedence

An important finding during testing: unlike Linux `iptables`, where rule *order* determines
which rule wins, Windows Defender Firewall gives **Block rules unconditional precedence over
Allow rules** regardless of specificity — a Block-Any rule overrides even a more specific
Allow rule for a single IP. To produce three independent, unambiguous test results, the two
rules were therefore toggled with `Enable-NetFirewallRule` / `Disable-NetFirewallRule` between
tests rather than left active simultaneously.

## Test Procedure and Results

### Test 1 — Permitted connection (authorised staff device → service)

- State: `Allow-Staff-5000` enabled, `Block-Others-5000` disabled
- Command run (on staff device / phone browser): navigate to `http://192.168.137.1:5000`
- Expected outcome: Connection succeeds, page loads
- Actual result: **Succeeded.** The phone loaded a directory listing of the project folder
  (`crypto_toolkit.py`, `filter_tests.md`, `report.pdf`, etc.), confirming the connection was
  permitted. See `evidence/test1_permitted.png`.

### Test 2 — Blocked connection (same device, after removing its permission)

- State: `Allow-Staff-5000` disabled, `Block-Others-5000` enabled
- Command run: reload `http://192.168.137.1:5000` from the same phone
- Expected outcome: Connection refused / times out
- Actual result: **Blocked as expected.** Browser returned
  `This site can't be reached — 192.168.137.1 took too long to respond (ERR_CONNECTION_TIMED_OUT)`.
  See `evidence/test2_blocked.png`.

### Test 3 — Blocked connection (repeat, confirming the block is consistent)

- State: same as Test 2 (`Block-Others-5000` enabled, no allow rule active)
- Command run: reload the same URL again
- Expected outcome: Connection refused / times out, consistent with Test 2
- Actual result: **Blocked, consistent with Test 2.**

> Limitation: only one spare physical device (a phone) was available for testing, rather than
> three separate hosts representing staff/guest/other networks. Tests 2 and 3 therefore both
> use the same device with its permission revoked, to demonstrate the block is consistent,
> rather than testing three distinct network segments. This is a reasonable substitute given
> the available equipment, and the underlying rule logic (allow one IP, block all others) is
> the same mechanism that would enforce guest vs staff network separation in a full deployment.

After testing, both rules were restored to their normal operating state (`Block-Others-5000`
enabled, `Allow-Staff-5000` enabled) so the service enforces the intended policy going forward.
