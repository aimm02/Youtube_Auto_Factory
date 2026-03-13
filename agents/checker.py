def self_correct(script):
    total_len = len(script.get('hook', '')) + len(script.get('content', '')) + len(script.get('cta', ''))
    
    if total_len > 1000:
        return False, "Naskah terlalu panjang."
    
    return True, "Passed"