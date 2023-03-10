
def check_and_replace(xpath):
        xpath=xpath.replace("'''", "")
        if("contains" in xpath):
            return xpath.replace('=',',')
        else:
            return xpath