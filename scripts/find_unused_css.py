#!/usr/bin/env python3
"""
Script to scan HTML files in the public folder and identify CSS rules
in themes/2026/static/css/main.css that are not used anywhere.

Usage: python scripts/find_unused_css.py
"""

import os
import re
from pathlib import Path


def parse_css_rules(css_content):
    """Parse CSS content and extract rules with proper handling of at-rules."""
    rules = []
    
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Track position for parsing
    i = 0
    
    while i < len(css_content):
        # Skip whitespace
        while i < len(css_content) and css_content[i] in ' \t\n\r':
            i += 1
        
        if i >= len(css_content):
            break
        
        # Check for at-rules (like @media, @keyframes, etc.)
        if css_content[i] == '@':
            # Find the at-rule name
            j = i + 1
            while j < len(css_content) and css_content[j].isalpha():
                j += 1
            at_name = css_content[i:j]
            
            # Find the opening brace
            brace_start = css_content.find('{', j)
            if brace_start == -1:
                i += 1
                continue
            
            # Find the closing brace (matching)
            brace_count = 1
            k = brace_start + 1
            while k < len(css_content) and brace_count > 0:
                if css_content[k] == '{':
                    brace_count += 1
                elif css_content[k] == '}':
                    brace_count -= 1
                k += 1
            
            rule_content = css_content[brace_start+1:k-1]
            rules.append({
                'type': 'at-rule',
                'name': at_name,
                'content': rule_content,
                'full_rule': css_content[i:k]
            })
            
            i = k
            continue
        
        # Regular rules
        brace_start = css_content.find('{', i)
        if brace_start == -1:
            break
        
        selector = css_content[i:brace_start].strip()
        
        # Find the closing brace (matching)
        brace_count = 1
        k = brace_start + 1
        while k < len(css_content) and brace_count > 0:
            if css_content[k] == '{':
                brace_count += 1
            elif css_content[k] == '}':
                brace_count -= 1
            k += 1
        
        if brace_count == 0:
            declarations = css_content[brace_start+1:k-1].strip()
            rules.append({
                'type': 'rule',
                'selector': selector,
                'declarations': declarations,
                'full_rule': css_content[i:k]
            })
        
        i = k
    
    return rules


def extract_selectors_from_rule_content(content):
    """Extract all selectors from within a rule (like @media content)."""
    selectors = []
    
    # Split by rules
    rule_pattern = r'([^{]+)\{([^}]*)\}'
    
    for match in re.finditer(rule_pattern, content):
        selector = match.group(1).strip()
        declarations = match.group(2).strip()
        if selector and declarations:
            selectors.append((selector, declarations))
    
    return selectors


def extract_html_classes_and_ids(html_content):
    """Extract all class names, IDs, and tags used in HTML."""
    used_selectors = set()
    
    # Extract class names
    class_pattern = r'class=["\']([^"\']+)["\']'
    for match in re.finditer(class_pattern, html_content):
        classes = match.group(1).split()
        for cls in classes:
            used_selectors.add(f'.{cls}')
            # Also add base class without modifiers
            base_cls = cls.split('-')[0] if '-' in cls else cls
            used_selectors.add(f'.{base_cls}')
    
    # Extract IDs
    id_pattern = r'id=["\']([^"\']+)["\']'
    for match in re.finditer(id_pattern, html_content):
        used_selectors.add(f'#{match.group(1)}')
    
    # Extract tag selectors (basic elements)
    tag_pattern = r'<([a-zA-Z][a-zA-Z0-9]*)'
    for match in re.finditer(tag_pattern, html_content):
        tag = match.group(1).lower()
        # Skip HTML structural tags
        if tag not in ('html', 'head', 'body', 'meta', 'link', 'script', 'style', 'title', 'noscript', 'doctype', '!--'):
            used_selectors.add(tag)
    
    # Extract data attributes
    data_attr_pattern = r'data-([a-z-]+)=["\'][^"\']*["\']'
    for match in re.finditer(data_attr_pattern, html_content):
        attr_name = match.group(1)
        used_selectors.add(f'[data-{attr_name}]')
    
    return used_selectors


def is_fundamental_selector(selector):
    """Check if selector is a fundamental HTML element or universal selector."""
    fundamental = {
        ':root', 'html', 'body', '*', '::before', '::after', '::selection',
        '::first-line', '::first-letter', '::placeholder', '::marker',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'div', 'span',
        'ul', 'li', 'nav', 'header', 'footer', 'main', 'section', 'article',
        'aside', 'button', 'input', 'select', 'textarea', 'form', 'table',
        'thead', 'tbody', 'tr', 'td', 'th', 'code', 'pre', 'blockquote',
        'svg', 'path', 'circle', 'rect', 'polygon', 'line', 'g', 'use',
        'small', 'strong', 'em', 'u', 's', 'del', 'ins', 'mark',
        'ol', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'picture', 'source',
        'video', 'audio', 'canvas', 'iframe', 'object', 'embed',
    }
    selector_lower = selector.lower().strip()
    return selector_lower in fundamental


def is_part_of_multi_selector(selector, full_rule):
    """Check if selector is part of a multi-part selector (like *, *::before, *::after)."""
    if ',' in full_rule and selector in full_rule:
        # Check if this selector is part of a comma-separated list
        parts = full_rule.split(',')
        for part in parts:
            part = part.strip()
            # Check if this part contains only fundamental selectors
            selectors = [s.strip() for s in part.split('{')[0].split(',')]
            all_fundamental = all(is_fundamental_selector(s) for s in selectors if s)
            if all_fundamental:
                return True
    return False


def is_js_activated_selector(selector):
    """Check if selector is activated by JavaScript (theme toggles, etc.)."""
    # These selectors are set by JS, not found in static HTML
    js_activated = [
        '[data-theme="dark"]', '[data-theme="light"]',
        '[data-active]', '[data-expanded]', '[data-collapsed]',
        '[data-selected]', '[data-current]',
    ]
    return selector.strip() in js_activated


def is_interaction_selector(selector):
    """Check if selector requires user interaction or state (hover, focus, etc.)."""
    interaction = {
        ':hover', ':focus', ':active', ':visited', ':focus-within', ':focus-visible',
        ':checked', ':disabled', ':enabled', ':required', ':optional', ':valid',
        ':invalid', ':placeholder-shown', ':target', ':lang(', ':not(:',
        '::placeholder', '::selection', '::first-line', '::first-letter',
        '::backdrop', '::file-selector-button',
    }
    selector_lower = selector.lower().strip()
    for pseudo in interaction:
        if pseudo in selector_lower:
            return True
    return False


def is_media_query_responsive(selector):
    """Check if selector is in a media query (responsive design)."""
    # These are responsive breakpoints that may apply conditionally
    responsive = [
        '@media (min-width:', '@media (max-width:',
        '@media (pointer:', '@media (hover:',
        '@media (prefers-color-scheme:', '@media (prefers-reduced-motion:',
    ]
    return any(selector.strip().startswith(q) for q in responsive)


def selector_matches_used(selector, used_selectors):
    """Check if a selector matches any of the used selectors."""
    selector_clean = selector.strip()
    
    # Skip fundamental selectors
    if is_fundamental_selector(selector_clean):
        return True
    
    # Skip interaction selectors (hover states, etc.)
    if is_interaction_selector(selector_clean):
        return True
    
    # Handle multiple selectors (comma-separated)
    if ',' in selector_clean:
        parts = [s.strip() for s in selector_clean.split(',')]
        return any(selector_matches_used(part, used_selectors) for part in parts)
    
    # Handle complex selectors with combinators
    combinators = [' ', '>', '+', '~']
    if any(c in selector_clean for c in combinators):
        # For descendant, child, adjacent sibling, or general sibling selectors,
        # check if the key selector exists
        parts = re.split(r'[>\s+~]+', selector_clean)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Remove pseudo-elements
            part = re.sub(r'::[\w-]+', '', part)
            # Check pseudo-classes
            if ':' in part:
                part = part.split(':')[0]
            if part and selector_matches_used(part, used_selectors):
                return True
        return False
    
    # Simple selector matching
    if selector_clean in used_selectors:
        return True
    
    # Check if it's an attribute selector
    if selector_clean.startswith('[') and selector_clean.endswith(']'):
        # Extract the attribute part
        attr_part = selector_clean[1:-1]
        # Check if any used selector contains this attribute
        for used in used_selectors:
            if used.startswith('[') and attr_part in used:
                return True
    
    # Check if selector starts with a used class or ID
    for used in used_selectors:
        if selector_clean.startswith(used) or used.startswith(selector_clean):
            return True
    
    # Check for class modifiers (e.g., .nav-card-blog matches .nav-card)
    if selector_clean.startswith('.'):
        base_class = selector_clean.split('-')[0] if '-' in selector_clean else selector_clean
        for used in used_selectors:
            if used.startswith(base_class):
                return True
    
    return False


def main():
    # Paths
    css_path = Path('themes/2026/static/css/main.css')
    public_path = Path('public')
    
    # Read CSS file
    print(f"Reading CSS from: {css_path}")
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Parse CSS rules
    rules = parse_css_rules(css_content)
    
    # Collect all selectors
    all_selectors = []
    for rule in rules:
        if rule['type'] == 'rule':
            selector = rule['selector']
            declarations = rule['declarations']
            full_rule = rule.get('full_rule', '')
            
            # Handle comma-separated selectors
            for sel in selector.split(','):
                sel = sel.strip()
                if sel:
                    # Check if this is part of a multi-selector with fundamental elements
                    is_multi = is_part_of_multi_selector(sel, full_rule)
                    all_selectors.append({
                        'selector': sel,
                        'declarations': declarations,
                        'is_fundamental_group': is_multi
                    })
        elif rule['type'] == 'at-rule' and rule['name'] in ['@media', '@supports']:
            # Extract nested rules
            nested_selectors = extract_selectors_from_rule_content(rule['content'])
            for sel, decl in nested_selectors:
                all_selectors.append({
                    'selector': sel,
                    'declarations': decl,
                    'is_fundamental_group': False
                })
    
    print(f"Found {len(all_selectors)} CSS selectors (after parsing)")
    
    # Scan all HTML files in public folder
    print(f"Scanning HTML files in: {public_path}")
    all_used_selectors = set()
    
    html_files = list(public_path.rglob('*.html'))
    print(f"Found {len(html_files)} HTML files")
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            used = extract_html_classes_and_ids(html_content)
            all_used_selectors.update(used)
        except Exception:
            pass  # Skip files that can't be read
    
    print(f"Found {len(all_used_selectors)} unique selectors in HTML")
    
    # Categorize selectors
    truly_used = []
    fundamentally_used = []  # Universal, HTML elements, box-sizing, etc.
    interaction_states = []  # :hover, :focus, etc.
    js_activated = []  # data-theme, etc.
    responsive = []  # Media query rules
    potentially_unused = []
    
    for item in all_selectors:
        selector = item['selector']
        declarations = item['declarations']
        
        if item.get('is_fundamental_group'):
            fundamentally_used.append((selector, declarations))
        elif selector_matches_used(selector, all_used_selectors):
            truly_used.append((selector, declarations))
        elif is_fundamental_selector(selector):
            fundamentally_used.append((selector, declarations))
        elif is_interaction_selector(selector):
            interaction_states.append((selector, declarations))
        elif is_js_activated_selector(selector):
            js_activated.append((selector, declarations))
        elif is_media_query_responsive(selector):
            responsive.append((selector, declarations))
        else:
            potentially_unused.append((selector, declarations))
    
    # Print results
    print(f"\n{'='*70}")
    print("CSS USAGE ANALYSIS RESULTS")
    print(f"{'='*70}\n")
    
    print(f"✅ DEFINITELY USED: {len(truly_used)} selectors")
    print(f"   (Found in HTML files)\n")
    
    print(f"⚙️  FUNDAMENTAL/UNIVERSAL: {len(fundamentally_used)} selectors")
    print(f"   (HTML elements, box-sizing, universal selectors)\n")
    
    print(f"👆 INTERACTION STATES: {len(interaction_states)} selectors")
    print(f"   (:hover, :focus, :active, etc.)\n")
    
    print(f"🔧 JS-ACTIVATED: {len(js_activated)} selectors")
    print(f"   (Set by JavaScript like dark mode toggle)\n")
    
    print(f"📱 RESPONSIVE/MEDIA QUERIES: {len(responsive)} rules")
    print(f"   (Mobile/tablet/desktop breakpoints)\n")
    
    if potentially_unused:
        print(f"{'='*70}")
        print(f"⚠️  POTENTIALLY UNUSED: {len(potentially_unused)} selectors")
        print(f"   (Not found anywhere in public HTML - review carefully)")
        print(f"{'='*70}\n")
        
        # Group by category
        by_category = {}
        for selector, declarations in potentially_unused:
            # Determine category
            if selector.startswith('.'):
                cat = 'Class selectors'
            elif selector.startswith('#'):
                cat = 'ID selectors'
            elif selector.startswith('['):
                cat = 'Attribute selectors'
            elif ':' in selector:
                cat = 'Pseudo selectors'
            elif '@' in selector:
                cat = 'At-rules'
            else:
                cat = 'Tag selectors'
            
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((selector, declarations))
        
        for cat, items in by_category.items():
            print(f"\n{cat}:")
            for selector, declarations in items:
                # Truncate long declarations
                decl_short = declarations[:100] + '...' if len(declarations) > 100 else declarations
                print(f"  {selector}")
                print(f"    → {decl_short}")
    else:
        print(f"\n{'='*70}")
        print(f"✅ NO UNUSED CSS FOUND!")
        print(f"All CSS selectors are either used or are fundamental/interactive/JS-activated.")
        print(f"{'='*70}\n")
    
    # Summary
    total_accounted = len(truly_used) + len(fundamentally_used) + len(interaction_states) + len(js_activated) + len(responsive)
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Total selectors analyzed: {len(all_selectors)}")
    print(f"Accounted for: {total_accounted} ({total_accounted/len(all_selectors)*100:.1f}%)")
    print(f"Potentially unused: {len(potentially_unused)} ({len(potentially_unused)/len(all_selectors)*100:.1f}%)")


if __name__ == '__main__':
    main()
