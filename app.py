import streamlit as st
import urllib.parse
import urllib.request
import json
import os

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
# Uses gapread-logo.png as the tab favicon if available
favicon_path = "gapread-logo.png" if os.path.exists("gapread-logo.png") else "📚"

st.set_page_config(
    page_title="GapRead | The Personal Progress Checklist",
    page_icon=favicon_path,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Silent Regional Routing
# ---------------------------------------------------------
MARKETPLACES = {
    "AU": {"domain": "amazon.com.au", "tag": "gapread-22"},
    "US": {"domain": "amazon.com",    "tag": "gapread-22"},  # update if you have a distinct -20 US tag
    "GB": {"domain": "amazon.co.uk", "tag": "gapread-22"},
    "CA": {"domain": "amazon.ca",    "tag": "gapread-22"},
    "DE": {"domain": "amazon.de",    "tag": "gapread-22"},
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_user_country_code() -> str:
    """Silently resolves user country code to route to the correct Amazon domain."""
    try:
        req = urllib.request.Request(
            "https://ipapi.co/json/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode())
            return data.get("country_code", "US")
    except Exception:
        return "US"


user_country = get_user_country_code()
active_market = MARKETPLACES.get(user_country, MARKETPLACES["US"])

# ---------------------------------------------------------
# Curated Library (Top 10 Inventory)
# ---------------------------------------------------------
BOOKS_DB = {
    "Health": [
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "asin": "0735211299",
            "description": "A practical framework for breaking destructive routines and establishing consistent physical baselines."
        },
        {
            "title": "Outlive: The Science and Art of Longevity",
            "author": "Dr. Peter Attia",
            "asin": "0593236599",
            "description": "Tactical breakdown of metabolic health, cardiovascular training, and nutritional biochemistry."
        },
        {
            "title": "Why We Sleep",
            "author": "Matthew Walker, PhD",
            "asin": "1501144324",
            "description": "A scientific analysis of cognitive restoration, physical recovery, and vital sleep architecture."
        },
        {
            "title": "Breath: The New Science of a Lost Art",
            "author": "James Nestor",
            "asin": "0735213615",
            "description": "Fascinating exploration of respiratory physiology, autonomic regulation, and cellular stamina."
        },
        {
            "title": "Built from Broken",
            "author": "Scott Hogan",
            "asin": "1735728509",
            "description": "A science-backed guide to healing joint pain, fixing posture, and bulletproofing connective tissue."
        }
    ],
    "Finance": [
        {
            "title": "The Psychology of Money",
            "author": "Morgan Housel",
            "asin": "0857197681",
            "description": "Crucial perspectives on risk tolerance, patience, and behavioral biases that govern wealth accumulation."
        },
        {
            "title": "I Will Teach You to Be Rich",
            "author": "Ramit Sethi",
            "asin": "1523505745",
            "description": "A structured personal finance framework for automating cash flow, investing, and eliminating debt."
        },
        {
            "title": "The Simple Path to Wealth",
            "author": "JL Collins",
            "asin": "153366792X",
            "description": "A clear, low-overhead blueprint for achieving financial independence through broad-market indexing."
        },
        {
            "title": "Die with Zero",
            "author": "Bill Perkins",
            "asin": "0358099765",
            "description": "Rethinking wealth optimization: maximizing memorable life experiences before health declines."
        },
        {
            "title": "Your Money or Your Life",
            "author": "Vicki Robin & Joe Dominguez",
            "asin": "0143115766",
            "description": "Transforming your relationship with money by calculating real hourly life energy exchanged for expenses."
        }
    ],
    "Happiness": [
        {
            "title": "Man's Search for Meaning",
            "author": "Viktor E. Frankl",
            "asin": "0807014273",
            "description": "An enduring exploration of finding purposeful drive and internal resilience in the face of suffering."
        },
        {
            "title": "The Courage to Be Disliked",
            "author": "Ichiro Kishimi & Fumitake Koga",
            "asin": "1501197274",
            "description": "Adlerian principles on shedding people-pleasing habits and taking ownership of your emotional state."
        },
        {
            "title": "Four Thousand Weeks: Time Management for Mortals",
            "author": "Oliver Burkeman",
            "asin": "0374159122",
            "description": "A sobering yet liberating look at time limits, letting go of perfectionism, and choosing what to ignore."
        },
        {
            "title": "The Antidote: Happiness for People Who Can't Stand Positive Thinking",
            "author": "Oliver Burkeman",
            "asin": "0865478015",
            "description": "An intelligent counter-narrative to toxic positivity, embracing uncertainty, failure, and realism."
        },
        {
            "title": "Flow: The Psychology of Optimal Experience",
            "author": "Mihaly Csikszentmihalyi",
            "asin": "0061339202",
            "description": "The foundational study on entering states of deep, absorbing engagement and everyday satisfaction."
        }
    ],
    "Social": [
        {
            "title": "How to Win Friends and Influence People",
            "author": "Dale Carnegie",
            "asin": "0671027034",
            "description": "The quintessential guide to empathetic listening, perspective-taking, and sincere human interaction."
        },
        {
            "title": "Crucial Conversations",
            "author": "Joseph Grenny et al.",
            "asin": "1260474186",
            "description": "Frameworks for navigating high-stakes personal and professional dialogue without anger or withdrawal."
        },
        {
            "title": "Never Eat Alone",
            "author": "Keith Ferrazzi",
            "asin": "0385346654",
            "description": "Building a generous, genuine professional and personal network centered on reciprocity."
        },
        {
            "title": "Nonviolent Communication: A Language of Life",
            "author": "Marshall B. Rosenberg, PhD",
            "asin": "189200528X",
            "description": "Resolving deep relational conflict by speaking to underlying unmet human needs rather than blame."
        },
        {
            "title": "Reclaiming Conversation: The Power of Talk in a Digital Age",
            "author": "Sherry Turkle",
            "asin": "0143109790",
            "description": "How to restore rich, face-to-face attention in family life, friendships, and work relationships."
        }
    ],
    "Spiritual": [
        {
            "title": "A Guide to the Good Life: The Ancient Art of Stoic Joy",
            "author": "William B. Irvine",
            "asin": "0195374614",
            "description": "Classical Stoic practices translated into pragmatic daily mental models for tranquility."
        },
        {
            "title": "The Untethered Soul",
            "author": "Michael A. Singer",
            "asin": "1572245379",
            "description": "Methods for detaching from relentless inner chatter and habitual stress triggers."
        },
        {
            "title": "Meditations",
            "author": "Marcus Aurelius (Gregory Hays Translation)",
            "asin": "0812968255",
            "description": "Direct personal journals on stoic duty, mental composure, and ethical self-discipline."
        },
        {
            "title": "Awareness: The Perils and Opportunities of Reality",
            "author": "Anthony de Mello",
            "asin": "0385249373",
            "description": "Short, incisive lectures on waking up from unconscious conditioning and psychological illusions."
        },
        {
            "title": "Waking Up: A Guide to Spirituality Without Religion",
            "author": "Sam Harris",
            "asin": "1451636024",
            "description": "Rigorous exploration of mindfulness and the nature of consciousness grounded in neuroscience."
        }
    ],
    "Gratitude / Charity": [
        {
            "title": "Doing Good Better",
            "author": "William MacAskill",
            "asin": "1592409660",
            "description": "How to allocate personal effort, capital, and charity for the greatest measurable real-world impact."
        },
        {
            "title": "The Power of Giving",
            "author": "Azim Jamal & Harvey McKinnon",
            "asin": "1585426189",
            "description": "The psychology of contribution and why service to others is fundamental to sustained well-being."
        },
        {
            "title": "Thanks! How Practicing Gratitude Can Make You Happier",
            "author": "Robert A. Emmons, PhD",
            "asin": "0547085737",
            "description": "Scientific research into how proactive gratitude habits physically alter stress response and outlook."
        },
        {
            "title": "The Life You Can Save",
            "author": "Peter Singer",
            "asin": "1983667793",
            "description": "A compelling moral argument for active philanthropy and living with an outward-looking focus."
        },
        {
            "title": "Grateful: The Transformative Power of Giving Thanks",
            "author": "Diana Butler Bass",
            "asin": "0062659472",
            "description": "Examining gratitude not as a self-help checklist, but as a social and moral habit of life."
        }
    ]
}


def build_book_url(book: dict) -> str:
    domain = active_market["domain"]
    tag = active_market["tag"]
    if book.get("asin"):
        return f"https://www.{domain}/dp/{book['asin']}?tag={tag}"
    query = urllib.parse.quote_plus(f"{book['title']} {book['author']}")
    return f"https://www.{domain}/s?k={query}&tag={tag}"


# ---------------------------------------------------------
# UI Header Banner & Value Proposition
# ---------------------------------------------------------
if os.path.exists("gapread-banner.png"):
    st.image("gapread-banner.png", use_container_width=True)
else:
    st.title("GapRead")
    st.caption("THE PERSONAL PROGRESS CHECKLIST")

st.markdown(
    """
    Most people read for entertainment or validation—rarely for targeted repair. 
    Your life does not stall evenly; it breaks down at your weakest link.

    Complete this 60-second personal progress checklist to isolate your single biggest bottleneck 
    and unlock your curated, top 10 targeted reading blueprint designed to bridge the gap.
    """
)

# ---------------------------------------------------------
# Progress Checklist Input Form
# ---------------------------------------------------------
with st.form("checklist_form"):
    st.markdown("#### Evaluate Your Fulfillment Baselines")
    st.caption("Be ruthlessly honest: 1 = critical bottleneck, 10 = peak mastery.")

    col1, col2 = st.columns(2)
    with col1:
        health_val = st.slider("🏃 Health & Physical Vitality", 1, 10, 4)
        finance_val = st.slider("💰 Financial Foundation & Cash Flow", 1, 10, 3)
        happiness_val = st.slider("☀️ Emotional Drive & Fulfillment", 1, 10, 6)
    with col2:
        social_val = st.slider("🤝 Relationships & Social Network", 1, 10, 8)
        spiritual_val = st.slider("🧘 Mental Resilience & Inner Calm", 1, 10, 6)
        charity_val = st.slider("🤲 Gratitude & Outward Contribution", 1, 10, 7)

    submitted = st.form_submit_button("Generate Strategic Reading Blueprint", use_container_width=True)

# ---------------------------------------------------------
# Output Rendering (Top 10 Engine)
# ---------------------------------------------------------
if submitted:
    ratings = {
        "Health": health_val,
        "Finance": finance_val,
        "Happiness": happiness_val,
        "Social": social_val,
        "Spiritual": spiritual_val,
        "Gratitude / Charity": charity_val
    }

    # Sort lowest to highest score (deficits prioritized)
    sorted_categories = sorted(ratings.items(), key=lambda x: x[1])

    target_count = 10
    selected_books = []
    pointers = {cat: 0 for cat in BOOKS_DB}

    # Round-robin selection through lowest-scoring pillars
    while len(selected_books) < target_count:
        added = False
        for category, score in sorted_categories:
            if len(selected_books) >= target_count:
                break
            ptr = pointers[category]
            catalog = BOOKS_DB[category]
            if ptr < len(catalog):
                book = catalog[ptr]
                pointers[category] += 1
                if not any(b["title"] == book["title"] for b in selected_books):
                    selected_books.append({**book, "category": category, "score": score})
                    added = True
        if not added:
            break

    st.markdown("---")
    st.markdown("### Your Custom Reading Checklist")
    st.caption("The 10 specific resources prioritized to patch your most critical life gaps right now.")

    for i, book in enumerate(selected_books, 1):
        url = build_book_url(book)

        with st.container(border=True):
            st.markdown(f"#### {i}. [{book['title']}]({url})")
            st.caption(f"**By {book['author']}** · Focus: *{book['category']}* (Current Level: {book['score']}/10)")
            st.write(book["description"])

            st.markdown(
                f'<a href="{url}" target="_blank" style="font-size: 0.9rem; text-decoration: none; color: #4F8BF9; font-weight: 500;">'
                f'Read overview & reviews ↗</a>',
                unsafe_allow_html=True
            )

    # Compliant, discreet footer disclosure
    st.markdown(
        "<div style='margin-top: 50px; text-align: center;'>"
        "<span style='color: #888888; font-size: 0.75rem;'>"
        "Disclosure: Some links on this page are affiliate links. If you choose to make a purchase, "
        "we may earn a small commission at no additional cost to you."
        "</span></div>",
        unsafe_allow_html=True
    )