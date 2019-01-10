
revoked_tokens = []

class RevokedTokenModel(object):
    """ Model class for revoked tokens """

    def add(self, jti):
        """ Function to save token identifier """
        revoked_tokens.append(jti)

    def is_blacklisted(self, jti):
        """ Function to check if token identifier is blacklisted """
        return bool(jti in revoked_tokens)
