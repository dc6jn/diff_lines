from Npp import editor, notepad, INDICATORSTYLE
import re

def highlight_consecutive_diffs():
    
    # Choose an indicator ID (8 to 31 are safe for custom scripts)
    INDICATOR_ID = 31 

    # 1. Define the visual style (e.g., a translucent box)
    editor.indicSetStyle(INDICATOR_ID, INDICATORSTYLE.ROUNDBOX) 

    # 2. Set the color (RGB tuple)
    editor.indicSetFore(INDICATOR_ID, (255, 100, 100)) # Red

    # 3. Set transparency (0 = fully transparent, 255 = fully opaque)
    editor.indicSetAlpha(INDICATOR_ID, 255)
    editor.indicSetOutlineAlpha(INDICATOR_ID, 255)

    # 4. CRITICAL: Force it to draw UNDER the text so the text doesn't get covered
    editor.indicSetUnder(INDICATOR_ID, True) 

    # 5. Set this indicator as active and apply it to your match
    editor.setIndicatorCurrent(INDICATOR_ID)
    # 1. Configure the visual style using the modern INDICATORSTYLE enum
    #editor.indicSetStyle(INDIC_ID, INDICATORSTYLE.ROUNDBOX)
    #editor.indicSetFore(INDIC_ID, (255, 100, 100))      # Soft Red (R, G, B)
    #editor.indicSetAlpha(INDIC_ID, 120)                 # Background transparency (0-255)
    #editor.indicSetOutlineAlpha(INDIC_ID, 255)          # Border transparency
    
    # Clear any previous highlights first
    #editor.setIndicatorCurrent(INDIC_ID)
    #editor.indicatorClearRange(0, editor.getTextLength())
    console.write("color coding\n" )
    editor.setIndicatorCurrent(INDICATOR_ID)
    editor.indicatorClearRange(0, editor.getTextLength())
    #editor.indicatorFillRange(0,100)
    
    num_lines = editor.getLineCount()
    if num_lines < 2:
        return
        
    # We will track tokens dynamically
    prev_tokens = []
    
    for line_idx in range(num_lines):
        # Retrieve the text and start position of the current line
        print(line_idx)
        line_text = editor.getLine(line_idx)
        line_start_pos = editor.positionFromLine(line_idx)
        
        # Parse non-whitespace chunks (hex bytes) and their actual offsets
        tokens = []
        for match in re.finditer(r'\S+', line_text):
            tokens.append({
                'val': match.group(),
                'start': line_start_pos + match.start(),
                'len': match.end() - match.start()
            })
            #print("Match group")
        # Compare with the line directly above
        if line_idx > 0:
            max_len = max(len(prev_tokens), len(tokens))
            for i in range(max_len):
                if i < len(tokens):
                    curr_tok = tokens[i]
                    #editor.indicatorFillRange(curr_tok['start'], curr_tok['start']+curr_tok['len'])
                    # Case 1: Byte has changed from the previous line
                    if i < len(prev_tokens):
                        if curr_tok['val'] != prev_tokens[i]['val']:
                            s1=curr_tok['start']
                            s2=curr_tok['len']
                            print("cN",s1,s2 )
                            editor.setIndicatorCurrent(INDICATOR_ID)
                            editor.indicatorFillRange(s1,s2)
                    
                    # Case 2: Byte is a new addition (the line grew longer)
                    else:
                        s1=curr_tok['start']
                        s2=curr_tok['len']
                        print("a",s1,s2)
                        editor.indicatorFillRange(s1,s2)
                        
        prev_tokens = tokens

# Run the highlight function
editor.indicatorClearRange(31, editor.getTextLength())
highlight_consecutive_diffs()
#editor.indicatorFillRange(0,100)
#editor.indicatorFillRange(8800, 8810)
#editor.scrollCaret()