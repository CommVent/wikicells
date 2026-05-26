# Trust model

> **Note**: This is a bootstrap mirror. Once the wiki is online, the canonical
> version of this content lives at `https://<TBD-domain>/wiki/Trust_Model`
> and this file becomes an auto-exported snapshot.

> **Status**: Designed, **not yet implemented**. Hello World uses only
> MediaWiki's stock access-level ladder. The model below is the target for
> the `TrustGraph` extension in a later phase.

## Problem

Wikipedia-style reputation is **earned** through activity and admin
discretion. There's no mechanism for an established user to **invest** their
reputation in a newer user to fast-track them — even Stack Overflow's bonus
on profile import is a one-time signal, not an ongoing stake.

We want a mechanism for trust transfer with **skin in the game**: vouching
should cost the voucher when it goes wrong, and reward them when it goes
right.

## The hybrid model

Four layers stacked together:

### 1. Earned floor (Wikipedia-style)

Autoconfirmed gates remain the floor. New accounts can't bypass minimum
account age and edit count without a vouch. This is anti-Sybil insurance.

### 2. Explicit vouching (Vouch-style)

A user with sufficient reputation can vouch for another user. A vouch
grants the vouchee a permission advance — they can bypass some autoconfirmed
gates immediately.

### 3. Stake-and-slash

Vouching locks up a fraction of the voucher's reputation. Two outcomes:

- **Vouchee thrives** (earns reputation organically through good
  contributions): the voucher's stake is returned **with bonus**. Vouching
  becomes a positive-sum action; vouchers are rewarded for picking well.
- **Vouchee misbehaves** (is sanctioned via revert, block, or RevisionDelete):
  the voucher loses a fraction of their staked reputation. Vouching is
  costly when it goes wrong; encourages careful vouches.

Vouches can be revoked by the voucher (with a cooldown) and slashes cascade
**partially**, not totally, up the chain — so a long-distance vouch chain
isn't catastrophic to top-of-graph users when a downstream vouchee
misbehaves.

### 4. Transitive propagation (EigenTrust-flavored)

Global reputation flows along the vouch graph with decay. A user's
reputation is a weighted combination of their earned reputation and the
flowed-in reputation from those who vouched for them. Decay prevents
unbounded amplification.

## Editor / oversighter tier

The top of the trust ladder — users with RevisionDelete and suppression
powers — is **granted by admins**, not earned by stake. This is a
deliberate capture-resistance measure: oversighter authority shouldn't be
purchasable with reputation.

## Worked example

> Alice has 1000 reputation. Bob is a new user.

- Alice vouches for Bob, staking 50 reputation. Alice now shows 950
  available + 50 staked-on-bob.
- Bob makes 20 good edits over a month, gaining 30 reputation organically.
- Alice's stake unlocks: she gets 50 back + a 10-rep bonus (for picking
  well). Alice now has 1010 available, 0 staked.
- *Alternative path*: Bob spams. After 3 reverted edits, Bob is sanctioned.
  Alice loses 25 of her 50 staked (50% slash). Alice now has 975 available.
- A small fraction also propagates up to anyone who vouched for Alice.

## Why not exactly off-the-shelf

- [mitchellh/vouch](https://github.com/mitchellh/vouch) has the vouching
  primitive but no stake-and-slash and no reputation propagation.
- [EigenTrust](https://nlp.stanford.edu/pubs/eigentrust.pdf) has the
  propagation math but no explicit vouching surface and no slashing.
- Web3 reputation projects have stake-and-slash but require crypto
  infrastructure that's overkill here.

So we build the synthesis as a custom MediaWiki extension (`TrustGraph`).
