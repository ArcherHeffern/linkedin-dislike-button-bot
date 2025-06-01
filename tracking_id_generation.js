function Qi(e, t) {
    return {
        pageUrn: Zi(e),
        trackingId: t || function (e) {
            for (var t, n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", i = [], r = 0, o = e.length, a = o % 3, s = o - a; r < s;)
                t = e[r] << 16,
                    t |= e[r + 1] << 8,
                    t |= e[r + 2],
                    i.push(n.charAt(t >>> 18 & 63)),
                    i.push(n.charAt(t >>> 12 & 63)),
                    i.push(n.charAt(t >>> 6 & 63)),
                    i.push(n.charAt(63 & t)),
                    r += 3
            switch (a) {
                case 2:
                    t = e[r] << 16,
                        t |= e[r + 1] << 8,
                        i.push(n.charAt(t >>> 18 & 63)),
                        i.push(n.charAt(t >>> 12 & 63)),
                        i.push(n.charAt(t >>> 6 & 63)),
                        i.push("=")
                    break
                case 1:
                    t = e[r] << 16,
                        i.push(n.charAt(t >>> 18 & 63)),
                        i.push(n.charAt(t >>> 12 & 63)),
                        i.push("="),
                        i.push("=")
            }
            return i.join("")
        }(Wi())
    }
}