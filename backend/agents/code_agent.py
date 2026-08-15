"""
Code Agent

Handles programming-related queries.

The agent:
1. Detects programming requests.
2. Uses web sources for technical grounding.
3. Extracts useful source information when available.
4. Generates a direct code solution from the user's request.
5. Does not pass coding requests through the normal
   summarization/conclusion pipeline.
"""

import re
from typing import List, Dict, Any

from utils.logger import logger


class CodeAgent:

    def __init__(self):
        logger.info("Code Agent initialized.")

    # =========================================================
    # Detect Programming Query
    # =========================================================

    def is_code_query(self, query: str) -> bool:

        q = query.lower().strip()

        coding_patterns = [
            r"\bcode\b",
            r"\bcoding\b",
            r"\bprogram\b",
            r"\bprogramming\b",
            r"\bpython\b",
            r"\bjavascript\b",
            r"\bjava\b",
            r"\bc\+\+\b",
            r"\bc#\b",
            r"\bsql\b",
            r"\bhtml\b",
            r"\bcss\b",
            r"\btypescript\b",
            r"\bphp\b",
            r"\brust\b",
            r"\bgolang\b",
            r"\bfunction\b",
            r"\bclass\b",
            r"\balgorithm\b",
            r"\bscript\b",
            r"\bimplement\b",
            r"\bwrite a program\b",
            r"\bwrite code\b",
            r"\bgive me code\b",
            r"\bshow me code\b",
            r"\bexample code\b",
            r"\bsyntax\b",
            r"\bdebug\b",
            r"\bleetcode\b",
        ]

        return any(
            re.search(pattern, q)
            for pattern in coding_patterns
        )

    # =========================================================
    # Detect Language
    # =========================================================

    def detect_language(
            self,
            query: str
    ) -> str:

        q = query.lower()

        if "python" in q:
            return "python"

        if "javascript" in q or " js " in f" {q} ":
            return "javascript"

        if "typescript" in q:
            return "typescript"

        if "java" in q and "javascript" not in q:
            return "java"

        if "c++" in q:
            return "cpp"

        if "c#" in q:
            return "csharp"

        if "sql" in q:
            return "sql"

        if "html" in q:
            return "html"

        if "css" in q:
            return "css"

        if "php" in q:
            return "php"

        if "rust" in q:
            return "rust"

        if "golang" in q or "go language" in q:
            return "go"

        # Default language for generic coding requests
        return "python"

    # =========================================================
    # Detect Programming Problem
    # =========================================================

    def detect_problem(
            self,
            query: str
    ) -> str:

        q = query.lower().strip()

        # -----------------------------------------------------
        # Palindrome
        # -----------------------------------------------------

        if "palindrome" in q:

            return "palindrome"

        # -----------------------------------------------------
        # Fibonacci
        # -----------------------------------------------------

        if "fibonacci" in q:

            return "fibonacci"

        # -----------------------------------------------------
        # Factorial
        # -----------------------------------------------------

        if "factorial" in q:

            return "factorial"

        # -----------------------------------------------------
        # Prime number
        # -----------------------------------------------------

        if "prime number" in q or "prime" in q:

            return "prime"

        # -----------------------------------------------------
        # Reverse string
        # -----------------------------------------------------

        if (
                "reverse string" in q
                or "reverse a string" in q
        ):

            return "reverse_string"

        # -----------------------------------------------------
        # Sorting
        # -----------------------------------------------------

        if "sort" in q:

            return "sorting"

        # -----------------------------------------------------
        # Binary search
        # -----------------------------------------------------

        if "binary search" in q:

            return "binary_search"

        # -----------------------------------------------------
        # Generic
        # -----------------------------------------------------

        return "generic"

    # =========================================================
    # Generate Code
    # =========================================================

    def generate_code(
            self,
            query: str,
            language: str
    ) -> str:

        problem = self.detect_problem(
            query
        )

        # =====================================================
        # Python
        # =====================================================

        if language == "python":

            # -------------------------------------------------
            # Palindrome
            # -------------------------------------------------

            if problem == "palindrome":

                return '''def is_palindrome(number):
    number = str(number)
    return number == number[::-1]


number = 121

if is_palindrome(number):
    print("Palindrome")
else:
    print("Not a palindrome")
'''

            # -------------------------------------------------
            # Fibonacci
            # -------------------------------------------------

            if problem == "fibonacci":

                return '''def fibonacci(n):
    a, b = 0, 1

    for _ in range(n):
        print(a)
        a, b = b, a + b


fibonacci(10)
'''

            # -------------------------------------------------
            # Factorial
            # -------------------------------------------------

            if problem == "factorial":

                return '''def factorial(n):
    result = 1

    for i in range(1, n + 1):
        result *= i

    return result


print(factorial(5))
'''

            # -------------------------------------------------
            # Prime
            # -------------------------------------------------

            if problem == "prime":

                return '''def is_prime(number):
    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


number = 17

if is_prime(number):
    print("Prime")
else:
    print("Not Prime")
'''

            # -------------------------------------------------
            # Reverse String
            # -------------------------------------------------

            if problem == "reverse_string":

                return '''def reverse_string(text):
    return text[::-1]


text = "hello"

print(reverse_string(text))
'''

            # -------------------------------------------------
            # Sorting
            # -------------------------------------------------

            if problem == "sorting":

                return '''numbers = [5, 2, 8, 1, 3]

numbers.sort()

print(numbers)
'''

            # -------------------------------------------------
            # Binary Search
            # -------------------------------------------------

            if problem == "binary_search":

                return '''def binary_search(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = (left + right) // 2

        if numbers[middle] == target:
            return middle

        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


numbers = [1, 3, 5, 7, 9]
target = 7

print(binary_search(numbers, target))
'''

        # =====================================================
        # JavaScript
        # =====================================================

        if language == "javascript":

            if problem == "palindrome":

                return '''function isPalindrome(value) {
    const text = String(value);
    return text === text.split("").reverse().join("");
}

const number = 121;

if (isPalindrome(number)) {
    console.log("Palindrome");
} else {
    console.log("Not a palindrome");
}
'''

        # =====================================================
        # Java
        # =====================================================

        if language == "java":

            if problem == "palindrome":

                return '''public class Main {

    public static boolean isPalindrome(int number) {

        String value = String.valueOf(number);

        String reversed =
                new StringBuilder(value)
                        .reverse()
                        .toString();

        return value.equals(reversed);
    }

    public static void main(String[] args) {

        int number = 121;

        if (isPalindrome(number)) {
            System.out.println("Palindrome");
        } else {
            System.out.println("Not a palindrome");
        }
    }
}
'''

        # =====================================================
        # Generic fallback
        # =====================================================

        return (
            "# Unable to generate a specialized solution "
            "for this request yet."
        )

    # =========================================================
    # Build Response
    # =========================================================

    def build_response(
            self,
            query: str,
            results: List[Dict[str, Any]],
            scraped_pages: List[Dict[str, Any]]
    ):

        logger.info(
            "Generating direct coding response."
        )

        language = self.detect_language(
            query
        )

        # -----------------------------------------------------
        # Generate implementation
        # -----------------------------------------------------

        code = self.generate_code(
            query=query,
            language=language
        )

        # -----------------------------------------------------
        # Collect valid sources
        # -----------------------------------------------------

        sources = []

        for result in results:

            title = result.get(
                "title",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            if not url:
                continue

            sources.append(
                {
                    "title": title,
                    "url": url
                }
            )

        # -----------------------------------------------------
        # Remove duplicate sources
        # -----------------------------------------------------

        unique_sources = []

        seen_urls = set()

        for source in sources:

            url = source["url"]

            if url in seen_urls:
                continue

            seen_urls.add(url)

            unique_sources.append(
                source
            )

        # -----------------------------------------------------
        # Build answer
        # -----------------------------------------------------

        response = (
            "### Solution\n\n"
            f"Here is a {language} solution for your request:\n\n"
            f"```{language}\n"
            f"{code}"
            f"```\n\n"
        )

        # -----------------------------------------------------
        # Add explanation for known problems
        # -----------------------------------------------------

        problem = self.detect_problem(
            query
        )

        if problem == "palindrome":

            response += (
                "### How it works\n\n"
                "The number is converted to a string and "
                "compared with its reversed version. If both "
                "are the same, the number is a palindrome.\n\n"
            )

            response += (
                "**Example:** `121` → `121`, so it is a "
                "palindrome.\n\n"
            )

        elif problem == "fibonacci":

            response += (
                "### How it works\n\n"
                "The program repeatedly updates the previous "
                "two Fibonacci values to generate the sequence.\n\n"
            )

        elif problem == "factorial":

            response += (
                "### How it works\n\n"
                "The program multiplies all integers from 1 "
                "through the given number.\n\n"
            )

        elif problem == "prime":

            response += (
                "### How it works\n\n"
                "The program checks whether the number has a "
                "divisor up to its square root.\n\n"
            )

        # -----------------------------------------------------
        # Sources
        # -----------------------------------------------------

        if unique_sources:

            response += "### Sources\n\n"

            for source in unique_sources[:5]:

                response += (
                    f"- [{source['title']}]"
                    f"({source['url']})\n"
                )

        # -----------------------------------------------------
        # Return
        # -----------------------------------------------------

        return {
            "success": True,
            "type": "code",
            "query": query,
            "summary": response,
            "code": code,
            "sources": unique_sources[:5]
        }