def cleanExtName(name,ext):
    return( name.split(".")[0] + "." + ext )

if __name__ == "__main__":
    print(cleanExtName('test.ext','pdf'))