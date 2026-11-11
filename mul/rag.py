# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""
Retrieval-augmented generation (RAG) and how to delete a person from it (Problem 21).

A RAG chatbot does not learn its documents into weights. It looks them up at answer time, so a person's data sits
in stores, and deleting from a store is exact. The catch is that the pipeline keeps many copies.

    make_tickets    a fictional support-ticket database (Fiona's tickets and everyone else's)
    tokens, chunk   lower-case words; overlapping word windows ("chunks") cut from each ticket
    HashEmbedder    hashed bag-of-words embedding. No training, so a chunk's vector depends only on its own text
    invert          recover words from an embedding with a word list: embeddings are not anonymous
    VectorIndex     exact cosine search with tombstones: delete() only marks a row, compact() removes it
    KeywordIndex    BM25 keyword search over an inverted index, with tombstones too
    IVFIndex        a small approximate index: k-means centroids and one list per centroid (the centroids are trained)
    AnswerCache     semantic cache: a new question close enough to an old one gets the old answer
    RAGStack        tickets -> chunks -> vectors + keywords; ask() = cache, hybrid search, answer, log;
                    forget(owner) deletes by owner ID from every store

Every stored item carries lineage (its ticket ID and its owner), because without it a deletion cannot find the copies.
"""

import re
import zlib
from collections import Counter

import numpy as np

# ---------------------------------------------------------------------------------------------
# A fictional support-ticket database
# ---------------------------------------------------------------------------------------------

# Public lists an attacker could also hold (like a phone book or a street map). Fiona's names are in them,
# as almost every name is in some public list.
FIRST_NAMES = ["amara", "ben", "chloe", "dev", "elif", "femi", "grace", "hamid", "isla", "jonah", "kavya", "liam",
               "mei", "noah", "olu", "pia", "quinn", "rohan", "sofia", "tariq", "uma", "vik", "wren", "yusuf",
               "zara", "fiona", "mila", "omar", "lucia", "kenji"]
SURNAMES = ["shah", "obi", "evans", "khan", "patel", "jones", "murphy", "ali", "brown", "singh", "clarke", "ward",
            "hughes", "rahman", "lewis", "kaur", "price", "bell", "das", "hall", "kowalczyk", "novak", "reyes",
            "haddad", "moreno", "sato"]
STREETS = ["oak lane", "mill road", "station street", "church walk", "park view", "river close", "high street",
           "elm grove", "kings avenue", "quarry hill", "larch row", "brook way"]

PRODUCTS = ["kettle", "toaster", "blender", "air fryer", "vacuum cleaner", "coffee machine", "microwave",
            "iron", "fan heater", "rice cooker"]
ISSUES = [("arrived broken", "sent a replacement"), ("has not arrived yet", "asked the courier to call you"),
          ("stopped working after a week", "booked a collection for repair"),
          ("came with a missing part", "posted the missing part"), ("is the wrong colour", "booked a return"),
          ("was charged to my card twice", "refunded the second payment")]
EXTRAS = ["i live at {house} {street}.", "the courier left it outside {house} {street} in the rain.",
          "i need it before the weekend.", "this is the second time this has happened.", "", ""]
OPENERS = ["hello, my {product} from order {order} {issue}.", "hi, the {product} i bought (order {order}) {issue}.",
           "order {order}. my new {product} {issue}."]

FIONA_TICKETS = [
    "hello, my air fryer from order 50417 arrived broken. i am in hospital for an operation until 3 march, so please "
    "do not send anything to 14 larch row before then. fiona kowalczyk, tel 555-0147. "
    "agent: sorry to hear that, fiona. we have paused the replacement for order 50417 until 4 march.",
    "hi, the replacement air fryer for order 50417 has not arrived yet. my daughter mila is collecting post at "
    "14 larch row while i am in hospital. fiona kowalczyk, tel 555-0147. "
    "agent: thank you, fiona. we have asked the courier to call mila.",
    "order 50417. the air fryer was charged to my card twice. please refund the second payment to my card ending 7731. "
    "fiona kowalczyk, tel 555-0147. agent: sorry, fiona. we have refunded the second payment.",
    "hi, the rice cooker i bought (order 51960) stopped working after a week. fiona kowalczyk, tel 555-0147. "
    "agent: sorry about this, fiona. we have booked a collection for repair.",
]
NEIGHBOUR_TICKET = ("hi, my toaster from order {order} has not arrived yet. the tracking says it was left with my "
                    "neighbour fiona kowalczyk at 14 larch row, but she is in hospital. {first} {last}, tel {phone}. "
                    "agent: sorry about this, {first}. we have asked the courier to call you.")


def make_tickets(n_customers=80, seed=0):
    """
    A fictional support-ticket database: a list of dicts with `ticket`, `owner`, `text`, `product`, `issue`,
    `order`, `first` and `last`. Every customer has 1 to 5 tickets. Fiona (owner "C-FIONA") has four, and one other customer
    (her neighbour) has a ticket that mentions her by name. Phone numbers are in 555-0100 to 555-0199, the range
    reserved for fiction, and nobody else has Fiona's number.
    """
    rng = np.random.default_rng(seed)
    firsts = [f for f in FIRST_NAMES if f not in ("fiona", "mila")]
    phones = [p for p in rng.permutation(100) if p != 47]
    orders = iter(rng.choice(np.arange(40000, 60000), 600, replace=False))
    rows = []
    for c in range(n_customers):
        first, last = firsts[rng.integers(len(firsts))], SURNAMES[rng.integers(20)]
        house, street, phone = int(rng.integers(1, 99)), STREETS[rng.integers(10)], f"555-01{phones[c]:02d}"
        for _ in range(int(rng.integers(1, 6))):
            product, (issue, action) = PRODUCTS[rng.integers(len(PRODUCTS))], ISSUES[rng.integers(len(ISSUES))]
            order = int(next(orders))
            text = (OPENERS[rng.integers(len(OPENERS))].format(product=product, order=order, issue=issue)
                    + " " + EXTRAS[rng.integers(len(EXTRAS))].format(house=house, street=street)).strip()
            text += f" {first} {last}, tel {phone}. agent: sorry about this, {first}. we have {action}."
            rows.append(dict(owner=f"C-{c:03d}", text=text, product=product, issue=issue, first=first, last=last,
                             order=order))
        if c == n_customers // 2:                            # Fiona's neighbour
            order = int(next(orders))
            rows.append(dict(owner=f"C-{c:03d}", product="toaster", issue="has not arrived yet", first=first, last=last,
                             order=order, text=NEIGHBOUR_TICKET.format(order=order, first=first, last=last, phone=phone)))
    for t in FIONA_TICKETS:
        product = "air fryer" if "air fryer" in t else "rice cooker"
        rows.append(dict(owner="C-FIONA", text=t, product=product, first="fiona", last="kowalczyk",
                         order=int(re.search(r"order (\d+)", t).group(1)), issue=next(i for i, _ in ISSUES if i in t)))
    rows = [rows[i] for i in rng.permutation(len(rows))]     # Fiona's tickets land among everyone else's
    for i, r in enumerate(rows):
        r["ticket"] = f"T{i:04d}"
    return rows


# ---------------------------------------------------------------------------------------------
# Text to vectors
# ---------------------------------------------------------------------------------------------

def tokens(text):
    """Lower-case words and numbers. '555-0147' becomes ['555', '0147']."""
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk(text, size=24, overlap=8):
    """Cut a text into windows of `size` words that overlap by `overlap` words."""
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


class HashEmbedder:
    """
    Hashed bag-of-words: each word goes to one of `dim` slots (a CRC32 hash), with a + or - sign, and the counts are
    scaled to length 1. Nothing is learned from the data, so a chunk's vector depends only on its own text.
    Neural embedders are frozen after training too, so the same holds for them.
    """

    def __init__(self, dim=4000):
        self.dim = dim

    def slot(self, word):
        h = zlib.crc32(word.encode())
        return h % self.dim, (1.0 if (h >> 16) & 1 else -1.0)

    def __call__(self, texts):
        V = np.zeros((len(texts), self.dim))
        for r, t in enumerate(texts):
            for w in tokens(t):
                b, s = self.slot(w)
                V[r, b] += s
        n = np.linalg.norm(V, axis=1, keepdims=True)
        return V / np.where(n == 0, 1, n)


def invert(embedder, v, candidates):
    """Words from `candidates` whose slot in `v` is non-zero with the right sign: a guess at the words behind v."""
    out = []
    for w in candidates:
        b, s = embedder.slot(w)
        if v[b] * s > 0:
            out.append(w)
    return out


# ---------------------------------------------------------------------------------------------
# Stores
# ---------------------------------------------------------------------------------------------

def _top(scores, ids, k):
    """Indices of the k best scores; ties are broken by ID, so the order of rows never matters."""
    return np.lexsort((np.asarray(ids), -scores))[:k]


class VectorIndex:
    """
    Exact cosine search (the rows are length 1, so a dot product is the cosine).
    delete() only sets a tombstone: the row stays in memory and in every snapshot until compact().
    """

    def __init__(self, dim):
        self.ids, self.owners = [], []
        self.V, self.alive = np.zeros((0, dim)), np.zeros(0, bool)

    def add(self, ids, owners, V):
        self.ids += list(ids)
        self.owners += list(owners)
        self.V = np.vstack([self.V, V])
        self.alive = np.r_[self.alive, np.ones(len(V), bool)]

    def delete(self, ids):
        hit = np.isin(np.asarray(self.ids, dtype=object), list(ids)) & self.alive
        self.alive &= ~hit
        return int(hit.sum())

    def search(self, q, k):
        if not self.ids:
            return []
        s = np.where(self.alive, self.V @ q, -np.inf)
        return [self.ids[i] for i in _top(s, self.ids, k) if self.alive[i]]

    def compact(self):
        keep = np.flatnonzero(self.alive)
        self.ids = [self.ids[i] for i in keep]
        self.owners = [self.owners[i] for i in keep]
        self.V, self.alive = self.V[keep], self.alive[keep]

    def snapshot(self):
        """What a backup of the index file holds: every stored row, tombstoned or not."""
        return dict(ids=list(self.ids), owners=list(self.owners), V=self.V.copy(), alive=self.alive.copy())

    def same_as(self, other):
        """True if both hold exactly the same (id, owner, vector) rows and no tombstones."""
        if not (self.alive.all() and other.alive.all()) or sorted(self.ids) != sorted(other.ids):
            return False
        a, b = np.argsort(self.ids), np.argsort(other.ids)
        return [self.owners[i] for i in a] == [other.owners[i] for i in b] and np.array_equal(self.V[a], other.V[b])


class KeywordIndex:
    """
    BM25 keyword search (Robertson & Zaragoza 2009) over an inverted index: term -> {chunk ID: count}.
    delete() only sets a tombstone. As in Lucene-based search engines, a tombstoned chunk is never returned but
    still counts in the term statistics until compact().
    """

    def __init__(self, k1=1.2, b=0.75):
        self.k1, self.b = k1, b
        self.postings, self.length, self.owner, self.dead = {}, {}, {}, set()

    def add(self, ids, owners, texts):
        self._purge(set(ids) & self.length.keys())          # a rewritten chunk that keeps its ID replaces the old one
        for i, o, t in zip(ids, owners, texts):
            toks = tokens(t)
            self.length[i], self.owner[i] = len(toks), o
            for w, c in Counter(toks).items():
                self.postings.setdefault(w, {})[i] = c

    def delete(self, ids):
        new = (set(ids) & self.length.keys()) - self.dead
        self.dead |= new
        return len(new)

    def df(self, term):
        """How many stored chunks contain the term (tombstoned ones included)."""
        return len(self.postings.get(term, {}))

    def search(self, query, k):
        n = len(self.length)
        if not n:
            return []
        avgdl = sum(self.length.values()) / n
        scores = {}
        for w in sorted(set(tokens(query))):
            p = self.postings.get(w)
            if not p:
                continue
            idf = np.log(1 + (n - len(p) + 0.5) / (len(p) + 0.5))
            for i, c in p.items():
                if i not in self.dead:
                    norm = c + self.k1 * (1 - self.b + self.b * self.length[i] / avgdl)
                    scores[i] = scores.get(i, 0.0) + idf * c * (self.k1 + 1) / norm
        return sorted(scores, key=lambda i: (-scores[i], i))[:k]

    def compact(self):
        self._purge(self.dead)

    def _purge(self, ids):
        for i in ids:
            del self.length[i], self.owner[i]
        for w in list(self.postings):
            p = self.postings[w]
            for i in ids & p.keys():
                del p[i]
            if not p:
                del self.postings[w]
        self.dead -= ids

    def same_as(self, other):
        return (not self.dead and not other.dead and self.postings == other.postings and self.length == other.length
                and self.owner == other.owner)


class IVFIndex:
    """
    Approximate nearest-neighbour search, the inverted-file (IVF) way: k-means puts every vector in one of
    `n_lists` lists, and a query searches only the `nprobe` lists with the closest centroids. The centroids are
    averages of the stored vectors, so they are a small trained model of the data. remove() takes rows out of
    the lists but leaves the centroids as they were; only a rebuild (fit again) retrains them.
    """

    def __init__(self, n_lists=16, iters=10, seed=0):
        self.n_lists, self.iters, self.seed = n_lists, iters, seed

    def fit(self, ids, V):
        order = np.argsort(ids)                                 # rows sorted by ID, so the insertion order never matters
        ids, V = [ids[i] for i in order], V[order]
        rng = np.random.default_rng(self.seed)
        C = V[rng.choice(len(V), self.n_lists, replace=False)].copy()
        for _ in range(self.iters):
            a = self._assign(V, C)
            for c in range(self.n_lists):
                if (a == c).any():
                    C[c] = V[a == c].mean(0)
        self.centroids, self.ids, self.V, self.list_of = C, list(ids), V.copy(), self._assign(V, C)
        return self

    @staticmethod
    def _assign(V, C):
        return (V @ (C / np.linalg.norm(C, axis=1, keepdims=True)).T).argmax(1)

    def remove(self, ids):
        keep = ~np.isin(np.asarray(self.ids, dtype=object), list(ids))
        self.ids, self.V, self.list_of = [i for i, k in zip(self.ids, keep) if k], self.V[keep], self.list_of[keep]
        return int((~keep).sum())

    def search(self, q, k, nprobe=2):
        probe = np.argsort(-(self.centroids @ q))[:nprobe]
        rows = np.flatnonzero(np.isin(self.list_of, probe))
        return [self.ids[rows[i]] for i in _top(self.V[rows] @ q, [self.ids[r] for r in rows], k)]


class AnswerCache:
    """
    Semantic cache: if a new question's embedding has cosine >= `threshold` with a cached question, the cached
    answer is served without searching again. Each entry keeps the chunk IDs and owners it was built from.
    """

    def __init__(self, threshold=0.75):
        self.threshold, self.entries = threshold, []

    def get(self, qv):
        if not self.entries:
            return None
        sims = np.array([e["qv"] @ qv for e in self.entries])
        best = int(sims.argmax())
        return self.entries[best] if sims[best] >= self.threshold else None

    def put(self, query, qv, answer, chunks, owners):
        self.entries.append(dict(query=query, qv=qv, answer=answer, chunks=list(chunks), owners=set(owners)))

    def invalidate(self, chunks=(), owner=None):
        """Drop every entry built from any of `chunks`, or tagged with `owner`. Returns how many went."""
        chunks = set(chunks)
        before = len(self.entries)
        self.entries = [e for e in self.entries if not (chunks & set(e["chunks"]) or owner in e["owners"])]
        return before - len(self.entries)


# ---------------------------------------------------------------------------------------------
# The whole chatbot
# ---------------------------------------------------------------------------------------------

def answer(query, texts):
    """A tiny extractive 'generator': the sentence from the retrieved chunks that shares most words with the query."""
    q = set(tokens(query))
    sentences = [s for t in texts for s in re.split(r"(?<=[.?!])\s+|\n", t) if s.strip()]
    if not sentences:
        return "sorry, i could not find anything about that."
    return max(sentences, key=lambda s: len(q & set(tokens(s))))


class RAGStack:
    """
    A support chatbot's retrieval stack. Stores: the ticket database, the chunk store, a vector index, a keyword
    index, an answer cache and the logs. Every chunk ID is '<ticket>/<n>' and every item carries its owner.
    """

    def __init__(self, embedder, size=24, overlap=8, k=3, cache_threshold=0.75):
        self.embed, self.size, self.overlap, self.k = embedder, size, overlap, k
        self.tickets, self.chunks, self.logs = {}, {}, []
        self.vectors, self.keywords = VectorIndex(embedder.dim), KeywordIndex()
        self.cache = AnswerCache(cache_threshold)

    def add_tickets(self, rows):
        new = []
        for r in rows:
            self.tickets[r["ticket"]] = dict(owner=r["owner"], text=r["text"])
            for j, c in enumerate(chunk(r["text"], self.size, self.overlap)):
                cid = f"{r['ticket']}/{j}"
                self.chunks[cid] = dict(ticket=r["ticket"], owner=r["owner"], text=c)
                new.append(cid)
        self.vectors.add(new, [self.chunks[c]["owner"] for c in new], self.embed([self.chunks[c]["text"] for c in new]))
        self.keywords.add(new, [self.chunks[c]["owner"] for c in new], [self.chunks[c]["text"] for c in new])
        return self

    def retrieve(self, query, k=None, depth=10):
        """Hybrid search: vector and keyword results merged by reciprocal rank fusion (Cormack et al. 2009)."""
        score = {}
        for hits in (self.vectors.search(self.embed([query])[0], depth), self.keywords.search(query, depth)):
            for rank, cid in enumerate(hits):
                score[cid] = score.get(cid, 0.0) + 1 / (60 + rank)
        return sorted(score, key=lambda c: (-score[c], c))[:k or self.k]

    def ask(self, asker, query, record=True):
        """
        Answer a question: the cache first, then search and answer. Every question is cached and logged, unless
        record=False (used for our own test questions, so they leave no copies behind).
        """
        qv = self.embed([query])[0]
        hit = self.cache.get(qv)
        if hit is not None:
            chunks, owners, reply = hit["chunks"], hit["owners"] | {asker}, hit["answer"]
        else:
            chunks = self.retrieve(query)
            reply = answer(query, [self.chunks[c]["text"] for c in chunks])
            owners = {self.chunks[c]["owner"] for c in chunks} | {asker}
            if record:
                self.cache.put(query, qv, reply, chunks, owners)
        if record:
            self.logs.append(dict(asker=asker, query=query, chunks=list(chunks), owners=set(owners), answer=reply,
                                  cached=hit is not None))
        self.last_from_cache = hit is not None
        return reply

    def _drop(self, tickets, owner=None):
        tickets = set(tickets)
        cids = [c for c, v in self.chunks.items() if v["ticket"] in tickets]
        removed = {"ticket database": sum(self.tickets.pop(t, None) is not None for t in tickets),
                   "chunk store": sum(self.chunks.pop(c, None) is not None for c in cids),
                   "vector index": self.vectors.delete(cids), "keyword index": self.keywords.delete(cids),
                   "answer cache": self.cache.invalidate(cids, owner)}
        keep = [r for r in self.logs if not (set(r["chunks"]) & set(cids) or owner in r["owners"])]
        removed["logs"] = len(self.logs) - len(keep)
        self.logs = keep
        return removed

    def forget(self, owner):
        """Delete by owner ID from every store. The two indexes only get tombstones until compact()."""
        return self._drop([t for t, v in self.tickets.items() if v["owner"] == owner], owner)

    def redact(self, ticket, old, new):
        """Rewrite one ticket (for example to remove a mention of another person) and index it again."""
        row = dict(ticket=ticket, owner=self.tickets[ticket]["owner"],
                   text=self.tickets[ticket]["text"].replace(old, new))
        self._drop([ticket])
        return self.add_tickets([row])

    def compact(self):
        self.vectors.compact()
        self.keywords.compact()
        return self

    def copies(self, owner):
        """How many items in each store are tagged with `owner` (stored, whether searchable or not)."""
        return {"ticket database": sum(v["owner"] == owner for v in self.tickets.values()),
                "chunk store": sum(v["owner"] == owner for v in self.chunks.values()),
                "vector index": sum(o == owner for o in self.vectors.owners),
                "keyword index": sum(o == owner for o in self.keywords.owner.values()),
                "answer cache": sum(owner in e["owners"] for e in self.cache.entries),
                "logs": sum(owner in r["owners"] for r in self.logs)}

    def scan(self, needles):
        """
        Look for any of the strings in `needles` in every store's raw contents, with no help from the tags.
        The indexes hold no text, so they are read the way an attacker would: the keyword index by its terms,
        the vector index with invert() (a row matches if every word of a needle is in it).
        """
        hit = lambda s: any(n in s for n in needles)
        in_kw = set()
        for n in needles:
            docs = [set(self.keywords.postings.get(t, {})) for t in tokens(n)]
            in_kw |= set.intersection(*docs) if docs else set()
        slots = [[self.embed.slot(t) for t in tokens(n)] for n in needles]
        in_vec = [any(all(v[b] * s > 0 for b, s in sl) for sl in slots) for v in self.vectors.V]
        return {"ticket database": sum(hit(v["text"]) for v in self.tickets.values()),
                "chunk store": sum(hit(v["text"]) for v in self.chunks.values()),
                "vector index": int(sum(in_vec)), "keyword index": len(in_kw),
                "answer cache": sum(hit(e["query"] + " " + e["answer"]) for e in self.cache.entries),
                "logs": sum(hit(r["query"] + " " + r["answer"]) for r in self.logs)}
