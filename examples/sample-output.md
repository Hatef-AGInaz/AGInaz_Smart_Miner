# Synthetic page: before and after

The example is a small, local HTML fixture, not a scraped commercial site.
It has two identical navigation blocks, a product table, a relative link, a
JSON-LD object, and an inline script. The demonstration records the output of
the local cleaner; it is not a live execution of the private engine.

| Measurement | Characters |
| --- | ---: |
| Raw HTML fixture | 473 |
| Clean extraction input, including source URL and title | 309 |

These measurements describe this fixture only. They do not measure tokens,
model cost, or performance across websites.

## Cleaned Markdown

```markdown
[Navigation](https://example.test/)

# Catalog

Available products and prices.

| Name | Price |
| --- | --- |
| Laptop | 12 |

[Product details](https://example.test/item/1)
```

The source URL is `https://example.test/catalog/`. The document also retains
the parsed JSON-LD claim `{ "@type": "Product", "name": "Laptop" }`
separately. The inline script is omitted, and the repeated navigation block
appears once. `example.test` is an illustrative address.

The complete extraction input additionally includes the source URL, page
title, and JSON-LD. A second extraction can use that same saved document;
the page need not be fetched again.
