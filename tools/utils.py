def deduplicate_results(results):
    seen_urls = set()
    unique_results = []

    for r in results:
        url = r.get("url")  # ✅ SAFE ACCESS

        # If URL exists → deduplicate
        if url:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(r)

        # If NO URL → still keep result
        else:
            unique_results.append(r)

    return unique_results
