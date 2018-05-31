DefaultDbName = 'tt_code_redemption'
RedeemErrors = Enum('Success, CodeDoesntExist, CodeIsInactive, CodeAlreadyRedeemed, AwardCouldntBeGiven, TooManyAttempts, SystemUnavailable, ')
RedeemErrorStrings = {
    RedeemErrors.Success: 'Success', # The code worked!
    RedeemErrors.CodeDoesntExist: 'Invalid code', # Invalid code
    RedeemErrors.CodeIsInactive: 'Code is inactive', # Inactive code
    RedeemErrors.CodeAlreadyRedeemed: 'Code has already been redeemed', # You already redeemed this
    RedeemErrors.AwardCouldntBeGiven: 'Award could not be given', # Award couldn't be given
    RedeemErrors.TooManyAttempts: 'Too many attempts, code ignored', # You tried too much
    RedeemErrors.SystemUnavailable: 'Code redemption is currently unavailable' } # Redeeming codes is unavailable for now
MaxCustomCodeLen = config.GetInt('tt-max-custom-code-len', 16)
