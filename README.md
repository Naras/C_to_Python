# C_to_Python_like_Indian_programming_languages
This project stared as a simple parser/converter that converter C statements to Python statements, with some special conversions of 1) functions like strcmp, strcpy, strcat to &lt;var> == &lt;expression> or &lt;var> = &lt;string expression> or &lt;var> += &lt;string expression> 2) structs to classes with a) __init__ (with assignments self.&lt;struct_member> = None), b) get (returns a dictionary with all struct members) and c) __str__ functions

Now, we extend this to design/construct "Indian Programming Languages" by:
transforming C Programs into Python-style programs where
1. keywords(tokens) like "if", "else", "while", "switch/case", "return", "type", "integer", "char" etc are replaced with equivalent keywords in Kannada (ಹೀಗಿದ್ದರೆ, ಇಲ್ಲದಿದ್ದರೆ, ಹೀಗಿರುವತನಕ, ಹಿಂತಿರುಗಿಸು, ಮಾದರಿ, ಪೂರ್ಣಾಂಕ, ಅಕ್ಷರಮಾಲೆ) or Sanskrit(यदि, अन्यथा, यदा, प्रतिदा, प्रकारः, पूर्णांकः, अक्षरंमाला).
2. Other Indian language keywords can easily be added into the multi-language dictionary in a .csv file and read into the transformer.
3. Variables/Identifiers can be in Indian langauge alphabets (varṇamāla) (unicode strings). This is not truly valid in C99, but we'll allow it. C99 allows identifiers in the style 'char \u0c80\u0c8f[] = "Hello World ಕನ್ನಡ संस्कृतं";'
4. The C-like input is properly parsed according to C grammar and a Python-grammar compliant output is produced.
