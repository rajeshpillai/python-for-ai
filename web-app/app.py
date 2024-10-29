import streamlit as st

# Data representing the course details
course_details = {
    "title": "Python Programming for DS + AI + ML",
    "subTitle": "The Foundations",
    "concepts": [
        {
            "sequence": 1,
            "title": "Introduction to Python",
            "description": "Learn what Python is, its applications, and how to install Python. Write your first Python program.",
            "url": "https://colab.research.google.com/drive/1MXxpTMXsz2IpvtGO8yIo-07B3noRP48M?usp=sharing",
            "open_in_new_window": True
        },
        {
            "sequence": 1.1,
            "title": "Bonus - 1 - The Real ChatBOT",
            "description": "Build chatbot using open-ai.",
            "url": "https://colab.research.google.com/drive/1IQbDVAPQQEb6qTm7ebGWMOTNOTUCh0tq?usp=sharing",
            "open_in_new_window": True
        },
        {
            "sequence": 1.2,
            "title": "Bonus - 2 - Know the Future",
            "description": "Your Horoscope",
            "url": "",
            "open_in_new_window": True
        },
        {
            "sequence": 1.3,
            "title": "Bonus - 3 - Your Personal Translator",
            "description": "Though shall speak and AI will translate",
            "url": "",
            "open_in_new_window": True
        },
        {
            "sequence": 2,
            "title": "Understanding Variables and Data Types",
            "description": "Explore variables, assigning values, and basic data types like integers, floats, strings, booleans, and None.",
            "url": "variables.html"
        },
        {
            "sequence": 3,
            "title": "Basic Arithmetic and Logical Operators",
            "description": "Learn about mathematical operations (addition, subtraction, multiplication, etc.) and logical operations like and, or, not.",
            "url": "operators.html"
        },
        {
            "sequence": 4,
            "title": "User Input and Output",
            "description": "Understand how to get input from the user and display output using the print function.",
            "url": "input-output.html"
        },
        {
            "sequence": 5,
            "title": "Conditional Statements",
            "description": "Learn how to use if, elif, and else statements to make decisions in your Python programs.",
            "url": "conditional-statements.html"
        },
        {
            "sequence": 6,
            "title": "Loops: for and while",
            "description": "Learn how to use for and while loops to repeat actions, and how to iterate over data structures.",
            "url": "loops.html"
        },
        {
            "sequence": 7,
            "title": "Functions and Code Reusability",
            "description": "Understand how to define and use functions to organize and reuse code efficiently.",
            "url": "functions.html"
        },
        {
            "sequence": 8,
            "title": "Lists, Tuples, and Sets",
            "description": "Learn how to store and manipulate collections of data using lists, tuples, and sets.",
            "url": "lists-tuples-sets.html"
        },
        {
            "sequence": 9,
            "title": "Dictionaries and Key-Value Pairs",
            "description": "Understand how to work with dictionaries, a powerful data structure for storing key-value pairs.",
            "url": "dictionaries.html"
        },
        {
            "sequence": 10,
            "title": "Exception Handling",
            "description": "Learn how to handle errors and exceptions in Python to write more robust programs.",
            "url": "exception-handling.html"
        },
        {
            "sequence": 11,
            "title": "Working with Files: Basics",
            "description": "Learn how to open, read, write, and close files in Python, including understanding different file modes.",
            "url": "file-handling-basics.html"
        },
        {
            "sequence": 12,
            "title": "Reading and Writing Files",
            "description": "Work through practical examples of reading and writing files, including CSV files and text processing.",
            "url": "reading-writing-files.html"
        },
        {
            "sequence": 13,
            "title": "File Handling: Advanced Techniques",
            "description": "Learn advanced file handling techniques, including context managers and error handling when working with files.",
            "url": "file-handling-advanced.html"
        },
        {
            "sequence": 14,
            "title": "List Comprehension",
            "description": "Explore list comprehensions as a concise way to create and manipulate lists.",
            "url": "list-comprehension.html"
        },
        {
            "sequence": 15,
            "title": "Modules and Libraries",
            "description": "Learn how to use Python's standard libraries and import custom modules to extend the functionality of your programs.",
            "url": "modules-libraries.html"
        },
        {
            "sequence": 16,
            "title": "Object-Oriented Programming (OOP)",
            "description": "Get an introduction to OOP concepts such as classes, objects, methods, and attributes.",
            "url": "oop-introduction.html"
        },
        {
            "sequence": 17,
            "title": "Basic Algorithms: Sorting and Searching",
            "description": "Learn basic algorithms such as bubble sort and linear search to enhance problem-solving skills.",
            "url": "basic-algorithms.html"
        },
        {
            "sequence": 18,
            "title": "Recursion in Python",
            "description": "Understand recursion and how to solve problems by breaking them down into smaller, self-similar tasks.",
            "url": "recursion.html"
        },
        {
            "sequence": 19,
            "title": "Working with JSON Data",
            "description": "Learn how to work with JSON data, including reading and writing JSON files in Python.",
            "url": "json-handling.html"
        },
        {
            "sequence": 20,
            "title": "Final Project and Next Steps",
            "description": "Recap everything you've learned with a final project, and explore resources to continue your Python journey.",
            "url": "final-project.html"
        }
    ]
}

# Set up Streamlit page layout and title
st.set_page_config(layout="wide")
st.markdown(
    f"<h1 style='text-align: center; color: white;'>{course_details['title']}</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<h2 style='text-align: center; color: lightgray;'>{course_details['subTitle']}</h2>",
    unsafe_allow_html=True,
)

# Define style for sticky notes
st.markdown(
    """
    <style>
    .sticky-note {
        background-color: #ffec99;
        padding: 20px;
        border-radius: 10px;
        width: 200px;
        min-height: 200px;
        margin: 20px;
        display: inline-flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .sticky-note:hover {
        transform: rotate(3deg);
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
    }
    .sequence-number {
        font-size: 16px;
        font-weight: bold;
        color: red;
        background-color: white;
        border-radius: 50%;
        padding: 5px;
        position: absolute;
        top: -15px;
    }
    .iframe-container {
        width: 100%;
        height: 80vh;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display sticky notes for each concept
selected_concept = None

# Layout to place sticky notes in a grid
cols = st.columns(4)  # Adjust number of columns as needed
for index, concept in enumerate(course_details["concepts"]):
    # Dynamic columns to arrange notes in rows
    with cols[index % 4]:
        # Render sticky note as button
        if st.button(concept["title"]):
            selected_concept = concept  # Capture the selected concept when clicked

        # Add sticky note styling with HTML
        st.markdown(
            f"""
            <div class="sticky-note">
                <div class="sequence-number">{concept['sequence']}</div>
                <h3>{concept['title']}</h3>
                <p>{concept['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Show iframe or open URL in a new tab if `open_in_new_window` is True
if selected_concept:
    st.markdown("---")
    st.markdown(f"### {selected_concept['title']}")
    st.write(selected_concept['description'])

    # Open URL in new tab if `open_in_new_window` is True, else embed in iframe
    if selected_concept["url"]:
        if selected_concept["open_in_new_window"]:
            st.markdown(
                f"<a href='{selected_concept['url']}' target='_blank'>Open in New Tab</a>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<iframe src='{selected_concept['url']}' class='iframe-container'></iframe>",
                unsafe_allow_html=True,
            )
    else:
        st.info("This concept doesn't have an associated link.")
