def vers_range_to_list(pkg_name: str, vers_range: str) -> [str]:
    """Converts a range of versions to a list of available versions in range"""
    # verse_range format - https://docs.github.com/en/graphql/reference/objects#securityvulnerability
    if vers_range[0] == "=":
        # only one version
        return [vers_range[2:]]
    elif vers_range[0:2] == "<=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        return """SELECT * from table WHERE pkg_name=%s AND 
        (major_vers<%s OR 
        (major_vers=%s AND minor_vers<%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers <=%s))""", \
               (pkg_name, major_vers, major_vers, minor_vers, major_vers, minor_vers, minor_vers)
    elif vers_range[0] == "<":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        return """SELECT * from table WHERE pkg_name=%s AND 
        (major_vers<%s OR 
        (major_vers=%s AND minor_vers<%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers <%s))""", \
               (pkg_name, major_vers, major_vers, minor_vers, major_vers, minor_vers, minor_vers)
    elif vers_range[0:2] == ">=" and "<" in vers_range:
        # assumes valid range
        lower, upper = vers_range[3:].replace(" < ", "").split(",")
        lower_major_vers, lower_minor_vers, lower_patch_vers = lower.split(".")
        upper_major_vers, upper_minor_vers, upper_patch_vers = upper.split(".")
        # TODO: waiting to implement until definitely being used, pretty tedious code
        """
        Scenarios (incomplete)
        major version in between
        major version is low, minor is greater than low -> need major less than high or minor less than or patch
        major version is low, minor is low, patch is greater than low

        major version is high
        
        """
        raise "not implemented yet"
    elif vers_range[0:2] == ">=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        return """SELECT * from table WHERE pkg_name=%s AND 
        (major_vers>%s OR 
        (major_vers=%s AND minor_vers>%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers >=%s))""", \
               (pkg_name, major_vers, major_vers, minor_vers, major_vers, minor_vers, minor_vers)
    else:
        # unexpected
        pass

print(vers_range_to_list("numpy", "<= 1.2.3"))
print(vers_range_to_list("numpy", ">= 1.2.3, < 4.5.6"))