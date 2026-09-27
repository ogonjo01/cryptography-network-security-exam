# Risk Assessment

## 1. Assets, Vulnerabilities, and Consequences

| # | Asset | Vulnerability | Possible Consequence |
|---|-------|----------------|------------------------|
| 1 | Central student records server | Weak staff passwords | Unauthorized access to student records, data theft or tampering |
| 2 | File transfer between campuses | Unencrypted file transfers | Interception of records in transit (eavesdropping / man-in-the-middle) |
| 3 | Records server network access | Guest network access to the records server | An unauthenticated device on the guest network could reach and attack the server |



## 2. Risk Ranking (Likelihood × Impact)

| Rank | Risk | Likelihood | Impact | Reasoning |
|------|------|------------|--------|-----------|
| 1 | Guest network access to the records server | High | High | The IT team has already observed repeated connection attempts from an unfamiliar external address, showing active probing is occurring now, not just theoretically possible. Because the guest network can reach the records server directly, any device on that network — including an attacker who joins it — has a path straight to sensitive data. High likelihood (active attempts already seen) combined with high impact (direct access to all student records) makes this the top priority. |
| 2 | Weak staff passwords | Medium | High | Weak passwords are common and easy to guess or brute-force, so likelihood is at least medium even without direct evidence of an attempt. Impact is high because a compromised staff account could grant legitimate-looking access to the server, bypassing other controls and making the intrusion harder to detect. |
| 3 | Unencrypted file transfers between campuses | Medium | Medium | Intercepting traffic between campuses requires the attacker to already have some network position (e.g. on a shared/guest segment), which is a precondition met by risk 1, so likelihood is medium rather than immediate. Impact is medium-to-high (records could be read or altered in transit) but is somewhat contained since it's exposure of data in motion, not full server compromise. |

Ranking rationale: Risk 1 is placed first because it is the only risk with direct evidence of
active exploitation attempts in the scenario (the repeated connections from an unfamiliar
external address), making it both the most likely and most urgent to close off. Risks 2 and 3
are both plausible but rely on an attacker either guessing credentials or being positioned to
intercept traffic, which the scenario doesn't confirm is already happening.

## 3. Recommended Controls

| Risk | Recommended Control |
|------|----------------------|
| Weak staff passwords | Enforce a password policy (minimum length/complexity) and multi-factor authentication |
| Unencrypted file transfers | Use an encrypted transfer protocol (e.g. SFTP/SCP or TLS) instead of plain FTP |
| Guest network access to records server | Network segmentation — place the records server on a VLAN/subnet not reachable from the guest network, enforced by firewall rules |


