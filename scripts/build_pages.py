import os
import textwrap
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..", "pages")

# Utility helpers

def sanitize_filename(name: str) -> str:
    sanitized = name.replace("/", "-")
    sanitized = sanitized.replace(":", "_")
    sanitized = sanitized.replace(" ", "_")
    return sanitized


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_page(path: str, content: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content.strip() + "\n")


def build_article_content(title: str, category: str, summary: str, see_also: list[str]) -> str:
    short_description = summary.split(".")[0]
    see_also_links = "\n".join(f"* [[{link}]]" for link in see_also)
    objectives = textwrap.dedent(
        f"""
        # Review the [[Category:{category}|{category}]] standards that apply to {title}.
        # Apply the guidance at your current base and log results on the [[Player Support Hub]].
        # Share feedback with teammates via in-game chat or the community channels.
        """
    ).strip()
    strategies = textwrap.dedent(
        f"""
        * Focus on how '''{title}''' supports long-term progress on [[play.2bz.org]].
        * Combine this guidance with insights from [[2bZ Server Overview]] and [[Quick Access Portal]].
        * Align preparation with travel routes listed in [[Transport Planner Hub]].
        """
    ).strip()
    collaboration = textwrap.dedent(
        f"""
        Players document their findings on '''{title}''' to keep the [[Community Showcase Index]] current. Coordinate with nearby builders, scouts, and logisticians so the whole faction benefits from the refined workflow.
        """
    ).strip()
    content = f"""
{{{{Short description|{short_description}}}}}
= {title} =
{{{{2bZ Navbox}}}}
__TOC__

== Overview ==
{textwrap.fill(summary, width=90)}

== Core Strategies ==
{strategies}

== Action Checklist ==
{objectives}

== Collaboration Opportunities ==
{textwrap.fill(collaboration, width=90)}

== See Also ==
{see_also_links}

[[Category:{category}]]
[[Category:2bZ Wiki]]
"""
    return textwrap.dedent(content).strip()


def build_category_content(category: str, description: str, pages: list[str]) -> str:
    bullet_list = "\n".join(f"* [[{page}]]" for page in sorted(pages))
    content = f"""
{{{{Short description|Overview of the {category} pages on the 2bZ wiki}}}}
= Category:{category} =
{{{{2bZ Navbox}}}}
__NOTOC__

{description}

== Featured Pages ==
{bullet_list}

[[Category:2bZ Wiki]]
"""
    return textwrap.dedent(content).strip()


def build_general_page(title: str, summary: str, sections: list[tuple[str, list[str]]]) -> str:
    short_description = summary.split(".")[0]
    sections_text = []
    for heading, bullets in sections:
        block = "\n".join(f"* {item}" for item in bullets)
        sections_text.append(f"== {heading} ==\n{block}")
    joined_sections = "\n\n".join(sections_text)
    content = f"""
{{{{Short description|{short_description}}}}}
= {title} =
{{{{2bZ Navbox}}}}
__TOC__

{textwrap.fill(summary, width=90)}

{joined_sections}

[[Category:2bZ Wiki]]
"""
    return textwrap.dedent(content).strip()


categories = {
    "Newcomer Guides": {
        "description": "Guides that help new arrivals on play.2bz.org settle in, make smart first-day decisions, and integrate with the wider survival community.",
        "topics": [
            "Orientation Tour",
            "Spawn Basics",
            "Starter Kit Setup",
            "First Night Survival",
            "Safe Logout Practices",
            "Community Chat Etiquette",
            "Protecting Temporary Bases",
            "Travel Safety Planning",
            "Early Resource Priorities",
            "Performance Optimization",
            "Managing Hunger",
            "Crafting Essentials",
            "Tool Durability Planning",
            "Respawn Planning",
            "Secret Storage Options",
            "Shared Resource Rooms",
            "Anarchy Survival Mindset",
            "Setting Personal Goals",
            "Sustainable Progress Habits",
        ],
    },
    "Quick Start Tutorials": {
        "description": "Condensed tutorials for rapidly gearing up, securing loot, and joining community initiatives without delay.",
        "topics": [
            "Gathering Food Quickly",
            "Building Shelter Fast",
            "Iron Rush Mining",
            "Portal Sprint Preparation",
            "Enchanting Basics",
            "Brewing Stand Setup",
            "Villager Rescue Workflow",
            "Boat Travel Mastery",
            "Horse Taming Basics",
            "Elytra Acquisition Prep",
            "Ender Chest Setup",
            "Trading Hall Basics",
            "XP Farming Quickstart",
            "Shield Mastery",
            "Armor Upgrade Path",
            "Weapon Enchantment Path",
            "Potion Loadout Planning",
            "Travel Kit Packing",
            "Emergency Escape Plans",
        ],
    },
    "Survival Handbook": {
        "description": "Long-form survival references for thriving through harsh weather, mob-packed nights, and long expeditions across 2bZ.",
        "topics": [
            "Long-Term Food Security",
            "Waterway Navigation",
            "Weather Preparedness",
            "Base Camouflage",
            "Inventory Management",
            "Night Patrol Routines",
            "Underground Shelter Design",
            "Surface Scouting",
            "Seasonal Migration Plans",
            "Supply Cache Networks",
            "Remote Farming",
            "Sustainable Mining Routes",
            "Endurance Travel",
            "Emergency Medical Supplies",
            "Fire Resistance Planning",
            "Raid Response",
            "Backup Gear Kits",
            "Signal Beacon Usage",
            "Safehouse Rotation",
        ],
    },
    "Combat Academy": {
        "description": "PvP tactics, training regimens, and combat-ready loadouts for defending bases and contesting objectives.",
        "topics": [
            "Swordplay Fundamentals",
            "Axe Combat Tactics",
            "Bow Control Drills",
            "Crossbow Ambushes",
            "Shield Counterplay",
            "Potion Duels",
            "Totem Management",
            "Gapple Timing",
            "Trident Combat",
            "Crystal PvP Basics",
            "Anchor Trap Planning",
            "Team Fight Formations",
            "Potion Splash Support",
            "Arena Training Layouts",
            "Gear Repair Cycles",
            "Escape and Pursuit",
            "Obsidian Box Defense",
            "End Crystal Etiquette",
            "Debuff Management",
        ],
    },
    "Resource Gathering": {
        "description": "Resource acquisition plans for every major material needed to maintain mega-projects and faction stockpiles.",
        "topics": [
            "Iron Ore Routes",
            "Coal Vein Mapping",
            "Diamond Hunt Strategy",
            "Redstone Prospecting",
            "Gold Rush Planning",
            "Lapis Lazuli Runs",
            "Emerald Trading Routes",
            "Ancient Debris Recovery",
            "Quartz Harvesting",
            "Netherite Upgrade Prep",
            "Clay Collection",
            "Sand Quarry Operations",
            "Gravel Dredging",
            "Obsidian Harvest",
            "Ice Gathering",
            "Wood Farm Rotation",
            "Wool Harvesting",
            "Mob Loot Stockpiles",
            "Alchemy Ingredient Runs",
        ],
    },
    "Building Styles": {
        "description": "Architectural references that highlight the server's most popular design languages and how to replicate them.",
        "topics": [
            "Modern Spawn Builds",
            "Medieval Fortresses",
            "Underground Hideouts",
            "Skybase Concepts",
            "Ocean Monument Renovations",
            "Desert Oasis Retreats",
            "Forest Village Homesteads",
            "Mountain Strongholds",
            "Floating Island Retreats",
            "Ruined City Aesthetic",
            "Industrial Complexes",
            "Steampunk Workshops",
            "Minimalist Survival Bases",
            "High-Tech Labs",
            "Futuristic Transit Hubs",
            "Organic Terraformed Bases",
            "Lore Museum Layouts",
            "PvP Arena Architecture",
            "Community Marketplaces",
        ],
    },
    "Infrastructure Projects": {
        "description": "Large-scale logistical builds that keep travel, trading, and communications functioning smoothly across 2bZ.",
        "topics": [
            "Overworld Highway Grid",
            "Nether Highway Upkeep",
            "Spawn Bypass Routes",
            "Portal Hub Engineering",
            "Map Art Galleries",
            "Public Farm Nexus",
            "Waypoint Obelisks",
            "Storage Array Planning",
            "Rail System Expansion",
            "Ice Boat Expressways",
            "Beacon Pyramid Network",
            "Border Watchposts",
            "Logistics Command Centers",
            "Resupply Depot Layouts",
            "Emergency Shelter Chain",
            "Underground Transit Lines",
            "Signal Tower Network",
            "End Gateway Integration",
            "Maintenance Scheduling",
        ],
    },
    "Farms & Automation": {
        "description": "Automated farms that fuel faction war chests and keep day-to-day necessities stocked.",
        "topics": [
            "Auto Wheat Farm",
            "Carrot Harvest Cycle",
            "Potato Yield Optimizer",
            "Melon and Pumpkin Stack",
            "Sugar Cane Array",
            "Bamboo Furnace Fuel",
            "Kelp Smelting Loop",
            "Mob Grinder Layout",
            "Guardian Farm Operations",
            "Wither Skeleton Farm",
            "Iron Golem Foundry",
            "Gold Piglin Farm",
            "Blaze Rod Refinery",
            "Shulker Shell Loop",
            "Raid Farm Scheduling",
            "Villager Crop Farm",
            "Honeycomb Production",
            "Wool Color Matrix",
            "Moss Block Mulcher",
        ],
    },
    "Redstone Mechanics": {
        "description": "Redstone devices, circuitry explanations, and component libraries for builders of every skill level.",
        "topics": [
            "Redstone Clock Library",
            "Observer Pulse Chains",
            "Piston Door Catalog",
            "Secret Entrance Logic",
            "Chunk Loader Basics",
            "Flying Machine Variants",
            "Item Sorter Arrays",
            "Signal Strength Math",
            "Comparator Tricks",
            "Hopper Line Optimization",
            "Note Block Alerts",
            "Trap Design Principles",
            "Elevator Blueprints",
            "Hidden Stair Mechanisms",
            "Pulse Extender Patterns",
            "Toggle Latch Showcase",
            "Wireless Redstone Concepts",
            "Lag-Friendly Circuits",
            "Testing Sandbox Setup",
        ],
    },
    "Exploration Logs": {
        "description": "Field notes and scouting reports from ambitious explorers charting the overworld beyond spawn.",
        "topics": [
            "Spawn Ring Survey",
            "Jungle Expedition Report",
            "Mesa Frontier Notes",
            "Taiga Recon Log",
            "Swampland Findings",
            "Frozen Peaks Traverse",
            "Savanna Trail Guide",
            "Ocean Monument Recon",
            "Mushroom Island Catalog",
            "Deep Dark Expedition",
            "Ancient City Findings",
            "Lush Cave Survey",
            "Badlands Ruin Mapping",
            "Mega Taiga Archives",
            "Dripstone Cavern Notes",
            "Sunken Ship Registry",
            "Village Network Mapping",
            "Stronghold Watchlist",
            "Rare Structure Sighting",
        ],
    },
    "Nether Expeditions": {
        "description": "Strategies and maps for navigating the Nether safely while controlling blaze, wither skeleton, and piglin encounters.",
        "topics": [
            "Nether Spawn Hub Guide",
            "Bastion Reconnaissance",
            "Fortress Control Plan",
            "Crimson Forest Logistics",
            "Warped Forest Safety",
            "Soul Sand Valley Prep",
            "Basalt Delta Navigation",
            "Piglin Trading Outposts",
            "Strider Ferry Routes",
            "Lava Lake Crossings",
            "Nether Roof Access",
            "Ancient Debris Scouting",
            "Wither Hunt Camps",
            "Blaze Spawner Tactics",
            "Ender Pearl Collection",
            "Nether Weathering Plan",
            "Portal Link Calibration",
            "Return Route Safeguards",
            "Resource Cache Locations",
        ],
    },
    "End Dimension Strategies": {
        "description": "Long-term End planning, from gateway linking to chorus farm layouts and raid staging grounds.",
        "topics": [
            "End Spawn Platform Safety",
            "Gateway Ring Mapping",
            "Elytra Expedition Routes",
            "Outer End Settlements",
            "Shulker Combat Guide",
            "Chorus Farm Design",
            "Dragon Fight Reset",
            "Enderman XP Hub",
            "Void Safety Measures",
            "Obsidian Pillar Mining",
            "Return Portal Logistics",
            "End City Loot Routing",
            "End Gateway Transit",
            "Enderman Proofing",
            "End Ship Salvage",
            "Dragon Egg Archive",
            "Falling Hazard Mitigation",
            "End Biome Catalog",
            "Ender Chest Supply Chain",
        ],
    },
    "Economy Systems": {
        "description": "Documentation of the barter, gift, and trade systems that keep supplies circulating despite the anarchy setting.",
        "topics": [
            "Barter Kit Templates",
            "Supply Drop Protocols",
            "Donation Chest Etiquette",
            "Resource Share Tracking",
            "Collective Farm Funding",
            "Infrastructure Sponsorships",
            "Repair Service Pricing",
            "Map Art Marketplace",
            "Bounty Board Operations",
            "Logistics Contracting",
            "Auction Event Planning",
            "Loan Ledger Basics",
            "Material Exchange Rates",
            "Emergency Aid Network",
            "Restock Reminder System",
            "Trading Season Calendar",
            "Philanthropy Highlights",
            "Community Currency Concepts",
            "Inventory Audit Process",
        ],
    },
    "Trading Outposts": {
        "description": "Profiles of trusted trade hubs, negotiation tips, and the safeguards they rely on to stay open.",
        "topics": [
            "Spawn Market Plaza",
            "Northern Ice Bazaar",
            "Desert Caravan Stop",
            "Jungle Treehouse Exchange",
            "Mesa Freight Station",
            "Taiga Timber Depot",
            "Swamp Apothecary",
            "Mountain Forge Quarter",
            "Coastal Fishery Hub",
            "Skyport Trade Ring",
            "Ender Market Loop",
            "Nether Anchor Exchange",
            "Crimson Caravanserai",
            "Warped Grove Emporium",
            "Soul Valley Trading Post",
            "Basalt Delta Depot",
            "Piglin Pact Embassy",
            "Outlands Relay Station",
            "Hidden Black Market",
        ],
    },
    "Factions & Diplomacy": {
        "description": "Histories and operating procedures for long-standing factions, alliances, and peace accords across the server.",
        "topics": [
            "Founders Council Charter",
            "Spawn Guardians Pact",
            "Highway Collective",
            "Atlas Cartographers",
            "Night Watch Sentinels",
            "Redstone Syndicate",
            "Skybuilders League",
            "Lorekeepers Union",
            "Nomad Fellowship",
            "Farmers Cooperative",
            "Artisans Assembly",
            "Vanguard Militia",
            "Archivist Circle",
            "Nether Navigators",
            "Endfarer Alliance",
            "Peacekeeper Mediation",
            "Logistics Bureau",
            "Builders Accord",
            "Settlement Treaties",
        ],
    },
    "Community Events": {
        "description": "Seasonal showcases, competitions, and collaborative projects that bring the server together.",
        "topics": [
            "Spawn Festival",
            "Highway Repair Week",
            "Map Art Expo",
            "PvP Invitational",
            "Build Battle Series",
            "Lore Quest Marathon",
            "Treasure Hunt Circuit",
            "Charity Resource Drive",
            "Speedrun Showdown",
            "Elytra Race Cup",
            "Fishing Derby",
            "Redstone Fair",
            "Parkour Challenge",
            "Nether Sprint Rally",
            "End Expedition Relay",
            "Community Awards Night",
            "Storytelling Fireside",
            "Holiday Build Jam",
            "Anniversary Celebration",
        ],
    },
    "History & Lore": {
        "description": "Recorded history, legendary moments, and server folklore kept alive by dedicated archivists.",
        "topics": [
            "Server Founding Story",
            "First Highway Era",
            "Rise of the Guardians",
            "Nether Roof Opening",
            "Dragon Cycle Chronicles",
            "Great Map Art Wave",
            "Age of Expeditions",
            "Factions Peace Summit",
            "Economic Renaissance",
            "The Wither Incursion",
            "End Gateway Rush",
            "Cultural Archives",
            "Redstone Revolution",
            "Infrastructure Golden Age",
            "Builder Renaissance",
            "Portal Network Saga",
            "Settlement Diaspora",
            "Modernization Timeline",
            "Future Visions",
        ],
    },
    "Landmarks & Regions": {
        "description": "Point-of-interest dossiers covering megabuilds, natural wonders, and remote installations.",
        "topics": [
            "Spawn Obelisk Plaza",
            "Old Capital Ruins",
            "Crystal Ridge Keep",
            "Mushroom Coast Refuge",
            "Frostwall Citadel",
            "Emberstone Bastion",
            "Verdant Basin",
            "Sunspire Canyon",
            "Azurewind Harbor",
            "Obsidian Sanctuary",
            "Whispering Pines",
            "Shattered Mesa",
            "Gilded Savannah",
            "Luminous Caverns",
            "Voidwatch Outpost",
            "Skylight Sanctum",
            "Golem Valley",
            "Starfall Observatory",
            "Endwatch Bastion",
        ],
    },
    "Player Settlements": {
        "description": "Active bases and player-led communities, with onboarding info, rules of engagement, and visiting hours.",
        "topics": [
            "Spawn Commons",
            "Northwatch Hamlet",
            "Sunrise Station",
            "Deepwood Enclave",
            "Sandsea Collective",
            "Cliffside Borough",
            "Riverside Cooperative",
            "Skyreach Commune",
            "Frostgate Hamlet",
            "Glowstone Market",
            "Nether Refuge",
            "End Frontier Camp",
            "Nomad Encampment",
            "Lagless Haven",
            "Builder's Refuge",
            "Archivist Sanctum",
            "Vanguard Keep",
            "Harvest Hollow",
            "Beacon Heights",
        ],
    },
    "Transportation Network": {
        "description": "Blueprints and maintenance schedules for boats, rails, ice roads, and portal grids.",
        "topics": [
            "Overworld Canal System",
            "River Lock Engineering",
            "Ice Boat Speedway",
            "Rail Junction Atlas",
            "Horse Road Outposts",
            "Waypoint Marker Guide",
            "Nether Portal Registry",
            "Gateway Alignment",
            "Ender Pearl Staging",
            "Skybridge Maintenance",
            "Tunnel Boring Crew",
            "Highway Lighting Plan",
            "Rest Stop Amenities",
            "Logistics Scheduling",
            "Emergency Detours",
            "Road Sign Standards",
            "Repair Kit Logistics",
            "Cartography Integration",
            "Traffic Monitoring",
        ],
    },
    "Technical Reference": {
        "description": "Mechanics deep dives, server performance notes, and compatibility considerations for large projects.",
        "topics": [
            "Tick Rate Observations",
            "Mob Cap Management",
            "Chunk Loading Policy",
            "Entity Cramming Tests",
            "Redstone Lag Studies",
            "Block Update Control",
            "Simulation Distance Notes",
            "Client Optimization",
            "Server Hardware Profile",
            "Backups and Restores",
            "Version Upgrade Log",
            "Plugin Compatibility",
            "Command Reference",
            "Data Pack Catalog",
            "Anti-Grief Strategies",
            "Performance Benchmarking",
            "Bug Report Workflow",
            "Testing Sandbox",
            "Diagnostic Toolkit",
        ],
    },
    "Quality of Life Tools": {
        "description": "Mods, settings, and optional enhancements that improve readability and reduce grind while respecting server rules.",
        "topics": [
            "Client Settings Checklist",
            "Minimal HUD Setup",
            "Resource Pack Library",
            "Sound Tuning Guide",
            "Performance Mod Profiles",
            "Macro Policy Overview",
            "Replay Mod Usage",
            "Coordinate Tracking",
            "Waypoint Mods",
            "Inventory Tweaks",
            "Chat Filter Tools",
            "Lighting Enhancements",
            "Accessibility Options",
            "Screenshot Workflow",
            "Build Planning Apps",
            "Spawn Alert Systems",
            "AFK Notification Setup",
            "Cloud Backup Tips",
            "Device Sync Planning",
        ],
    },
    "Server Policies": {
        "description": "Codified expectations that keep gameplay fair, respectful, and creatively focused.",
        "topics": [
            "Community Charter",
            "Reporting Workflow",
            "Ban Appeal Guide",
            "Chat Conduct Rules",
            "Build Respect Etiquette",
            "Duplication Policy",
            "Client Modification Rules",
            "PvP Engagement Rules",
            "Map Art Attribution",
            "Lore Canon Guidelines",
            "Infrastructure Stewardship",
            "Event Hosting Policy",
            "Collaboration Etiquette",
            "New Player Mentoring",
            "Resource Claim Etiquette",
            "Security Incident Plan",
            "Content Creation Policy",
            "Privacy and Data Use",
            "Dispute Resolution Steps",
        ],
    },
    "Staff & Governance": {
        "description": "Internal procedures, escalation charts, and the volunteer roles that keep the network stable.",
        "topics": [
            "Staff Roles Overview",
            "Admin Duty Roster",
            "Moderator Playbook",
            "Support Ticket Flow",
            "Community Liaison Tasks",
            "Event Team Procedures",
            "Technical Operations",
            "Infrastructure Maintenance",
            "Security Response",
            "Training Curriculum",
            "Onboarding New Staff",
            "Staff Code of Conduct",
            "Communication Standards",
            "Audit Trail Logging",
            "Incident Review",
            "Volunteer Recognition",
            "Feedback Collection",
            "Public Reports",
            "Transparency Dashboard",
        ],
    },
}

GENERAL_PAGES = {
    "Main Page": {
        "summary": "Welcome hub for the 2bZ community wiki, featuring curated routes for builders, fighters, traders, and explorers.",
        "sections": [
            ("Start Here", [
                "Visit [[Newcomer Guide: Orientation Tour]] for first-day orientation.",
                "Review [[2bZ Server Overview]] to understand the survival philosophy.",
                "Browse [[Quick Access Portal]] for role-specific shortcuts.",
            ]),
            ("Active Highlights", [
                "Check [[Update & Patch Archive]] for the latest changelog.",
                "Submit builds to [[Community Showcase Index]].",
                "Coordinate travel via [[Transport Planner Hub]].",
            ]),
        ],
    },
    "2bZ Server Overview": {
        "summary": "Snapshot of server identity, playstyle, and expectations on the long-running 2bZ survival network.",
        "sections": [
            ("Core Pillars", [
                "Persistent survival world with community-driven infrastructure.",
                "Cooperative focus where players self-govern and document standards.",
                "Technical transparency through [[Technical Reference Index]].",
            ]),
            ("Related Guides", [
                "[[Category:Server Policies]] for official expectations.",
                "[[Community Governance Overview]] covering councils and volunteers.",
                "[[Resource Planning Dashboard]] outlining logistical priorities.",
            ]),
        ],
    },
    "Quick Access Portal": {
        "summary": "Role-based launcher offering curated shortcuts for builders, scouts, traders, and PvP specialists.",
        "sections": [
            ("Navigation", [
                "Builders start with [[Build Inspiration Gallery]] and [[Infrastructure Control Center]].",
                "Explorers browse [[Exploration Gateway]].",
                "PvP teams review [[Competitive Play Hub]].",
            ]),
            ("Support", [
                "Report issues through [[Player Support Hub]].",
                "Use [[Contributor Guide]] for editing standards.",
                "Plan events via [[Category:Community Events]].",
            ]),
        ],
    },
    "Server Timeline Overview": {
        "summary": "High-level chronology referencing the major eras documented within [[History & Lore]] articles.",
        "sections": [
            ("Milestone Index", [
                "[[Category:History & Lore]] curates era-specific writeups.",
                "[[Update & Patch Archive]] logs version upgrades.",
                "[[Community Governance Overview]] highlights leadership shifts.",
            ]),
            ("How to Contribute", [
                "Submit sources on the talk pages of key history entries.",
                "Coordinate interviews with veteran players via [[Player Support Hub]].",
                "Flag timeline gaps for archivists in [[Contributor Guide]].",
            ]),
        ],
    },
    "Player Support Hub": {
        "summary": "Centralized support center for reporting issues, requesting assistance, and accessing mentoring resources.",
        "sections": [
            ("Help Channels", [
                "Escalate incidents through [[Governance Record: Staff Roles Overview]].",
                "Consult [[Policy Guide: Reporting Workflow]] for formal submissions.",
                "Join mentoring initiatives described in [[Policy Guide: New Player Mentoring]].",
            ]),
            ("Knowledge Base", [
                "Link to [[Safety & Security Center]] for protective habits.",
                "Review [[Contributor Guide]] before updating documentation.",
                "Track resolutions via [[Governance Record: Transparency Dashboard]].",
            ]),
        ],
    },
    "Safety & Security Center": {
        "summary": "Best practices for keeping accounts safe, reducing grief risk, and protecting valuables in an open survival environment.",
        "sections": [
            ("Account Safety", [
                "Use unique passwords and enable account-level protections.",
                "Avoid suspicious downloads and keep clients updated.",
                "Report breaches promptly following [[Policy Guide: Security Incident Plan]].",
            ]),
            ("In-Game Security", [
                "Hide bases using [[Survival Handbook: Base Camouflage]].",
                "Rotate storage as outlined in [[Newcomer Guide: Secret Storage Options]].",
                "Coordinate patrols via [[Survival Handbook: Night Patrol Routines]].",
            ]),
        ],
    },
    "Build Inspiration Gallery": {
        "summary": "Curated showcase linking to standout architecture, terraforming, and public works across the server.",
        "sections": [
            ("Featured Styles", [
                "[[Building Style: Modern Spawn Builds]] and [[Building Style: Steampunk Workshops]].",
                "[[Building Style: Organic Terraformed Bases]] for landscape integration ideas.",
                "[[Building Style: Community Marketplaces]] supporting trade hubs.",
            ]),
            ("Share Your Work", [
                "Submit screenshots via [[Media Library]].",
                "Document specs on relevant [[Category:Building Styles]] pages.",
                "Coordinate tours through [[Category:Community Events]] listings.",
            ]),
        ],
    },
    "Competitive Play Hub": {
        "summary": "Coordination point for PvP events, arena listings, and competitive training material.",
        "sections": [
            ("Training Guides", [
                "Review [[Category:Combat Academy]] articles for drills.",
                "Use [[Combat Academy: Arena Training Layouts]] to set up practice spaces.",
                "Track gear maintenance using [[Combat Academy: Gear Repair Cycles]].",
            ]),
            ("Event Coordination", [
                "Sign up for [[Community Event: PvP Invitational]].",
                "Schedule scrims through [[Category:Community Events]] calendar.",
                "Share match VODs in [[Media Library]].",
            ]),
        ],
    },
    "Exploration Gateway": {
        "summary": "Explorer-focused landing page tying together scouting notes, survival plans, and structure dossiers.",
        "sections": [
            ("Plan Your Route", [
                "Start with [[Exploration Log: Spawn Ring Survey]].",
                "Log discoveries under [[Category:Exploration Logs]] entries.",
                "Coordinate returns using [[Nether Expedition: Return Route Safeguards]].",
            ]),
            ("Support Resources", [
                "Pack supplies listed in [[Survival Handbook: Endurance Travel]].",
                "Share maps within [[Transportation Route: Cartography Integration]].",
                "Archive findings at [[Community Showcase Index]].",
            ]),
        ],
    },
    "Resource Planning Dashboard": {
        "summary": "Live-updated index mapping resource guides to ongoing megaproject requests and stockpile levels.",
        "sections": [
            ("Supply Priorities", [
                "Coordinate with [[Category:Resource Gathering]] plans.",
                "Automate harvests via [[Category:Farms & Automation]] guides.",
                "Log deliveries at [[Infrastructure Project: Logistics Command Centers]].",
            ]),
            ("Project Support", [
                "Check [[Category:Infrastructure Projects]] to match build needs.",
                "Review [[Category:Economy Systems]] for sponsorship options.",
                "Update records through [[Economy System: Inventory Audit Process]].",
            ]),
        ],
    },
    "Community Showcase Index": {
        "summary": "Directory of featured builds, lore articles, and player achievements maintained by curators.",
        "sections": [
            ("Submit Features", [
                "Nominate builds from [[Build Inspiration Gallery]].",
                "Highlight stories from [[Category:History & Lore]].",
                "Link video coverage in [[Media Library]].",
            ]),
            ("Archive Structure", [
                "Organized by [[Category:Landmarks & Regions]].",
                "Tag contributions with relevant [[Category]] pages.",
                "Cross-reference faction efforts via [[Category:Factions & Diplomacy]].",
            ]),
        ],
    },
    "Infrastructure Control Center": {
        "summary": "Operations board for monitoring major public works, maintenance queues, and expansion priorities.",
        "sections": [
            ("Key Networks", [
                "[[Infrastructure Project: Overworld Highway Grid]] maintenance schedule.",
                "[[Infrastructure Project: Portal Hub Engineering]] tasks.",
                "[[Infrastructure Project: Signal Tower Network]] coverage map.",
            ]),
            ("Coordination", [
                "Assign crews via [[Infrastructure Project: Logistics Command Centers]].",
                "Log completed work in [[Infrastructure Project: Maintenance Scheduling]].",
                "Forecast resources through [[Resource Planning Dashboard]].",
            ]),
        ],
    },
    "Transport Planner Hub": {
        "summary": "Central routing planner for highways, waterways, flight corridors, and emergency detours.",
        "sections": [
            ("Routing Tools", [
                "Consult [[Transportation Route: Waypoint Marker Guide]].",
                "Review [[Transportation Route: Emergency Detours]].",
                "Sync with [[Transportation Route: Cartography Integration]].",
            ]),
            ("Traveler Support", [
                "Check rest stops via [[Transportation Route: Rest Stop Amenities]].",
                "Coordinate convoys through [[Transportation Route: Logistics Scheduling]].",
                "Report hazards at [[Player Support Hub]].",
            ]),
        ],
    },
    "Technical Reference Index": {
        "summary": "Master index linking to diagnostics, server metrics, and engineering briefs that inform large builds.",
        "sections": [
            ("Performance Monitoring", [
                "Track ticks with [[Technical Brief: Tick Rate Observations]].",
                "Mitigate lag via [[Technical Brief: Redstone Lag Studies]].",
                "Coordinate tests in [[Technical Brief: Testing Sandbox]].",
            ]),
            ("Documentation", [
                "Reference [[Technical Brief: Version Upgrade Log]].",
                "Audit [[Technical Brief: Plugin Compatibility]].",
                "Follow [[Technical Brief: Bug Report Workflow]].",
            ]),
        ],
    },
    "Media Library": {
        "summary": "Media archive covering screenshots, cinematics, and timelines that highlight the 2bZ community.",
        "sections": [
            ("Content Types", [
                "Screenshot submissions from [[Build Inspiration Gallery]].",
                "Event footage tied to [[Category:Community Events]].",
                "Lore documentaries referenced in [[Category:History & Lore]].",
            ]),
            ("Contribution Guidelines", [
                "Follow attribution standards in [[Policy Guide: Content Creation Policy]].",
                "Store metadata using [[Economy System: Inventory Audit Process]].",
                "Report takedown requests via [[Player Support Hub]].",
            ]),
        ],
    },
    "Community Governance Overview": {
        "summary": "Explainer covering councils, volunteer crews, and collaborative decision-making traditions on 2bZ.",
        "sections": [
            ("Governance Bodies", [
                "[[Faction Dossier: Founders Council Charter]].",
                "[[Faction Dossier: Logistics Bureau]].",
                "[[Governance Record: Community Liaison Tasks]].",
            ]),
            ("Participation", [
                "Attend forums advertised on [[Category:Community Events]].",
                "Submit proposals via [[Governance Record: Transparency Dashboard]].",
                "Track decisions in [[Governance Record: Incident Review]].",
            ]),
        ],
    },
    "Contributor Guide": {
        "summary": "Editing playbook that keeps articles consistent, sourced, and easy to maintain.",
        "sections": [
            ("Editorial Standards", [
                "Follow formatting from [[Main Page]].",
                "Add categories like [[Category:Newcomer Guides]] where relevant.",
                "Cite evidence from in-game screenshots or logs.",
            ]),
            ("Tools", [
                "Use [[QoL Tool: Device Sync Planning]] to copy notes.",
                "Track drafts in [[Technical Brief: Testing Sandbox]].",
                "Coordinate merges via [[Governance Record: Staff Roles Overview]].",
            ]),
        ],
    },
    "Update & Patch Archive": {
        "summary": "Rolling changelog summarizing plugin tweaks, content additions, and technical maintenance windows.",
        "sections": [
            ("How to Log Updates", [
                "Record date, time, and summary for each patch.",
                "Reference affected systems like [[Category:Infrastructure Projects]].",
                "Link related bug tickets from [[Technical Brief: Bug Report Workflow]].",
            ]),
            ("Research", [
                "Compare against [[Technical Brief: Version Upgrade Log]].",
                "Highlight impacts to [[Category:Economy Systems]].",
                "Notify players through [[Quick Access Portal]].",
            ]),
        ],
    },
}

CATEGORY_SUMMARY_OVERRIDES = {
    "Server Policies": "Overview of official policy, etiquette, and safety documentation for all participants.",
    "Staff & Governance": "Internal governance documentation ensuring transparency and accountability.",
}

CATEGORY_PAGE_DATA = {}
for cat_name, data in categories.items():
    article_titles = []
    for topic in data["topics"]:
        title = f"{cat_name[:-1] if cat_name.endswith('s') else cat_name}: {topic}" if cat_name in {"Farms & Automation", "Server Policies"} else f"{cat_name[:-1] if cat_name.endswith('s') else cat_name} Guide: {topic}"
        # Custom naming for certain categories to avoid awkward titles
        if cat_name == "Building Styles":
            title = f"Building Style: {topic}"
        elif cat_name == "Infrastructure Projects":
            title = f"Infrastructure Project: {topic}"
        elif cat_name == "Farms & Automation":
            title = f"Farm Build: {topic}"
        elif cat_name == "Redstone Mechanics":
            title = f"Redstone Mechanic: {topic}"
        elif cat_name == "Exploration Logs":
            title = f"Exploration Log: {topic}"
        elif cat_name == "Nether Expeditions":
            title = f"Nether Expedition: {topic}"
        elif cat_name == "End Dimension Strategies":
            title = f"End Strategy: {topic}"
        elif cat_name == "Economy Systems":
            title = f"Economy System: {topic}"
        elif cat_name == "Trading Outposts":
            title = f"Trading Outpost: {topic}"
        elif cat_name == "Factions & Diplomacy":
            title = f"Faction Dossier: {topic}"
        elif cat_name == "Community Events":
            title = f"Community Event: {topic}"
        elif cat_name == "History & Lore":
            title = f"History & Lore: {topic}"
        elif cat_name == "Landmarks & Regions":
            title = f"Landmark Profile: {topic}"
        elif cat_name == "Player Settlements":
            title = f"Settlement Profile: {topic}"
        elif cat_name == "Transportation Network":
            title = f"Transportation Route: {topic}"
        elif cat_name == "Technical Reference":
            title = f"Technical Brief: {topic}"
        elif cat_name == "Quality of Life Tools":
            title = f"QoL Tool: {topic}"
        elif cat_name == "Server Policies":
            title = f"Policy Guide: {topic}"
        elif cat_name == "Staff & Governance":
            title = f"Governance Record: {topic}"
        elif cat_name == "Newcomer Guides":
            title = f"Newcomer Guide: {topic}"
        elif cat_name == "Quick Start Tutorials":
            title = f"Quick Start: {topic}"
        elif cat_name == "Survival Handbook":
            title = f"Survival Handbook: {topic}"
        elif cat_name == "Combat Academy":
            title = f"Combat Academy: {topic}"
        elif cat_name == "Resource Gathering":
            title = f"Resource Guide: {topic}"
        CATEGORY_PAGE_DATA.setdefault(cat_name, []).append({"title": title, "topic": topic})

# Build article pages
articles_root = os.path.join(ROOT, "articles")
SUMMARY_TEMPLATES = {
    "Newcomer Guides": "{title} walks new survivors through the {topic_lower} aspect of spawn life so they can acclimate quickly and avoid early setbacks.",
    "Quick Start Tutorials": "{title} condenses the essentials of {topic_lower} into a rapid-fire checklist that gets players expedition-ready in under an hour.",
    "Survival Handbook": "{title} documents proven survival patterns for managing {topic_lower} during long sessions on play.2bz.org.",
    "Combat Academy": "{title} breaks down {topic_lower} with drills, recommended gear, and teamwork cues for contested fights.",
    "Resource Gathering": "{title} maps out optimal loops for sourcing {topic_lower} while minimizing risk and travel time.",
    "Building Styles": "{title} highlights signature design motifs, block palettes, and layout tips for the {topic_lower} aesthetic.",
    "Infrastructure Projects": "{title} serves as the operations brief for constructing and maintaining the {topic_lower} initiative.",
    "Farms & Automation": "{title} outlines reliable redstone layouts and harvest cycles for a sustainable {topic_lower} setup.",
    "Redstone Mechanics": "{title} catalogs wiring theory and component usage for {topic_lower} builds used across 2bZ.",
    "Exploration Logs": "{title} compiles field notes, coordinates, and hazards encountered while surveying the {topic_lower} region.",
    "Nether Expeditions": "{title} shares navigation strategies and combat prep specific to {topic_lower} missions in the Nether.",
    "End Dimension Strategies": "{title} prepares crews for {topic_lower} objectives in the End, covering transport, safety, and loot recovery.",
    "Economy Systems": "{title} explains how {topic_lower} keeps resources circulating between independent teams.",
    "Trading Outposts": "{title} documents services, security measures, and approach routes for the {topic_lower} exchange.",
    "Factions & Diplomacy": "{title} summarizes history, membership expectations, and diplomatic ties surrounding the {topic_lower} group.",
    "Community Events": "{title} captures format, signup steps, and highlight reels from the {topic_lower} celebration.",
    "History & Lore": "{title} records testimonies, archival screenshots, and major outcomes tied to the {topic_lower} era.",
    "Landmarks & Regions": "{title} profiles terrain features, builders, and logistics that make the {topic_lower} landmark notable.",
    "Player Settlements": "{title} lists resident guidelines, visitor etiquette, and amenities maintained at the {topic_lower} settlement.",
    "Transportation Network": "{title} explains maintenance plans, travel advisories, and integration points for the {topic_lower} route.",
    "Technical Reference": "{title} provides measurements, experiments, and recommended practices for {topic_lower} considerations.",
    "Quality of Life Tools": "{title} reviews approved configurations and onboarding instructions for the {topic_lower} enhancement.",
    "Server Policies": "{title} clarifies enforcement scope, rationale, and reporting expectations for {topic_lower}.",
    "Staff & Governance": "{title} details responsibilities, documentation workflows, and accountability steps for {topic_lower} duties.",
}

for cat_name, entries in CATEGORY_PAGE_DATA.items():
    cat_slug = sanitize_filename(cat_name.lower().replace(" & ", " and ").replace(" ", "-"))
    category_dir = os.path.join(articles_root, cat_slug)
    ensure_dir(category_dir)
    titles = [entry["title"] for entry in entries]
    for idx, entry in enumerate(entries):
        title = entry["title"]
        topic = entry["topic"]
        filename = sanitize_filename(title) + ".mediawiki"
        path = os.path.join(category_dir, filename)
        topic_lower = topic.lower()
        summary_template = SUMMARY_TEMPLATES.get(cat_name, "{title} captures collective knowledge about {topic_lower} for long-term archival.")
        summary = textwrap.dedent(
            summary_template.format(
                title=title,
                topic=topic,
                topic_lower=topic_lower,
                category=cat_name,
            )
        ).strip() + " This entry links back to [[Category:{category}|{category}]] for additional context.".format(category=cat_name)
        see_also = []
        for offset in (1, 2, 3):
            see_title = titles[(idx + offset) % len(titles)]
            if see_title != title:
                see_also.append(see_title)
        content = build_article_content(title, cat_name, summary, see_also[:3])
        write_page(path, content)

# Build category pages
category_root = os.path.join(ROOT, "categories")
ensure_dir(category_root)
for cat_name, data in categories.items():
    filename = sanitize_filename(cat_name) + ".mediawiki"
    description = data["description"]
    pages = [entry["title"] for entry in CATEGORY_PAGE_DATA[cat_name]]
    content = build_category_content(cat_name, description, pages)
    write_page(os.path.join(category_root, filename), content)

# Build general pages
general_root = os.path.join(ROOT, "general")
ensure_dir(general_root)
for title, data in GENERAL_PAGES.items():
    filename = sanitize_filename(title) + ".mediawiki"
    content = build_general_page(title, data["summary"], data["sections"])
    write_page(os.path.join(general_root, filename), content)

# Category:2bZ Wiki page
category_2bz_path = os.path.join(category_root, "2bZ_Wiki.mediawiki")
category_2bz_content = """
{{Short description|Umbrella category for all documentation on the 2bZ community wiki}}
= Category:2bZ Wiki =
{{2bZ Navbox}}
__NOTOC__

All published guides, histories, and technical briefs on this wiki include the [[Category:2bZ Wiki]] tag so that contributors can audit coverage quickly. Use the category links below to jump directly into a focus area.

== Primary Categories ==
* [[Category:Newcomer Guides]]
* [[Category:Quick Start Tutorials]]
* [[Category:Survival Handbook]]
* [[Category:Combat Academy]]
* [[Category:Resource Gathering]]
* [[Category:Building Styles]]
* [[Category:Infrastructure Projects]]
* [[Category:Farms & Automation]]
* [[Category:Redstone Mechanics]]
* [[Category:Exploration Logs]]
* [[Category:Nether Expeditions]]
* [[Category:End Dimension Strategies]]
* [[Category:Economy Systems]]
* [[Category:Trading Outposts]]
* [[Category:Factions & Diplomacy]]
* [[Category:Community Events]]
* [[Category:History & Lore]]
* [[Category:Landmarks & Regions]]
* [[Category:Player Settlements]]
* [[Category:Transportation Network]]
* [[Category:Technical Reference]]
* [[Category:Quality of Life Tools]]
* [[Category:Server Policies]]
* [[Category:Staff & Governance]]

[[Category:2bZ Wiki]]
""".strip()
write_page(category_2bz_path, category_2bz_content)

# Template page
template_root = os.path.join(ROOT, "templates")
ensure_dir(template_root)
template_content = """
<includeonly>{| class="wikitable" style="width:100%; background:#0b0d17; color:#f4f4f4; border:2px solid #3a6ea5;"
! colspan="3" style="text-align:center; font-size:1.4em; background:#1b2333;" | 2bZ Wiki Navigation
|-
| style="width:33%; vertical-align:top;" |
; Orientation
:[[Main Page]]
:[[Quick Access Portal]]
:[[Player Support Hub]]
:[[Safety & Security Center]]
| style="width:33%; vertical-align:top;" |
; Build & Explore
:[[Build Inspiration Gallery]]
:[[Infrastructure Control Center]]
:[[Exploration Gateway]]
:[[Transport Planner Hub]]
| style="width:33%; vertical-align:top;" |
; Reference
:[[Technical Reference Index]]
:[[Resource Planning Dashboard]]
:[[Community Governance Overview]]
:[[Update & Patch Archive]]
|-
| colspan="3" style="text-align:center; background:#1b2333;" | Categories: [[Category:Newcomer Guides]] · [[Category:Resource Gathering]] · [[Category:Community Events]] · [[Category:Technical Reference]]
|}</includeonly><noinclude>
{{Documentation|content=Navigation template linking the primary hubs of the 2bZ community wiki.}}
</noinclude>
""".strip()
write_page(os.path.join(template_root, "Template_2bZ_Navbox.mediawiki"), template_content)

print("Pages generated.")
