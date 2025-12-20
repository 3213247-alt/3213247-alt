#!/usr/bin/env python3
"""
Research script to gather information about actuarial career transitions
and age considerations from private company sources.
Focus: Consulting firms, insurance companies, actuarial recruitment firms
"""

import requests
import json
import time
from urllib.parse import quote

def search_web(query, max_results=10):
    """Search for information using web search"""
    # Note: This is a placeholder - actual implementation would use a search API
    # For now, we'll document what sources to check
    print(f"Searching for: {query}")
    return []

def main():
    """Main research function"""
    
    # Key private sector sources to investigate:
    sources = {
        "consulting_firms": [
            "Milliman career transition reports",
            "Towers Watson actuarial hiring",
            "Deloitte actuarial career paths",
            "PwC actuarial recruitment",
            "EY actuarial career changers",
            "Oliver Wyman actuarial market",
            "Aon actuarial hiring practices"
        ],
        "insurance_companies": [
            "MetLife actuarial career development",
            "Prudential actuarial hiring",
            "AIG actuarial career paths",
            "Allstate actuarial recruitment",
            "State Farm actuarial careers",
            "Progressive actuarial hiring"
        ],
        "recruitment_firms": [
            "DW Simpson actuarial market reports",
            "Actuarial Careers actuarial hiring trends",
            "Selby Jennings actuarial market",
            "Robert Half actuarial salary guides"
        ],
        "actuarial_organizations_private": [
            "Casualty Actuarial Society career resources",
            "Society of Actuaries career transition",
            "International Actuarial Association market reports"
        ]
    }
    
    research_questions = [
        "actuarial career change age 30 35",
        "actuarial career transition mid-career",
        "actuarial hiring age discrimination",
        "actuarial market welcomes newcomers",
        "actuarial career changers 2020s",
        "actuarial entry requirements career change",
        "actuarial exams sufficient career change",
        "actuarial tech skills required 2024"
    ]
    
    print("=" * 80)
    print("RESEARCH PLAN: Actuarial Career Transitions at Age 35")
    print("=" * 80)
    print("\nFocus: Private company sources only")
    print("Avoid: Government reports, universities, educational institutions")
    print("\nKey Questions:")
    print("1. Was it common for 30-year-olds to change to actuarial work by just passing exams?")
    print("2. Does the market still welcome newcomers at age 35?")
    print("3. What tech skills are now required beyond exams?")
    print("\n" + "=" * 80)
    
    print("\nSources to investigate:")
    for category, items in sources.items():
        print(f"\n{category.upper()}:")
        for item in items:
            print(f"  - {item}")
    
    print("\n" + "=" * 80)
    print("Research queries to execute:")
    for q in research_questions:
        print(f"  - {q}")
    
    return sources, research_questions

if __name__ == "__main__":
    sources, queries = main()
    print("\nResearch framework prepared.")
    print("Note: Actual web search implementation would require API access.")
