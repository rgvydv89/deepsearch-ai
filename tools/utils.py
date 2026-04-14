def deduplicate_results(results):
    seen_urls = set()
    unique_results = []

    for r in results:
        if r["url"] not in seen_urls:
            unique_results.append(r)
            seen_urls.add(r["url"])

    return unique_results

def clean_search_query(query: str, max_length=300):
    # Remove extra quotes
    query = query.replace('"', '').strip()

    # Keep only first 300 chars
    if len(query) > max_length:
        query = query[:max_length]

    return query