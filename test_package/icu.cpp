#include <unicode/utypes.h>
#include <unicode/ucol.h>
#include <unicode/ustring.h>

int main(int, char **)
{
    UErrorCode status = U_ZERO_ERROR;
    UCollator *collator = ucol_open("ru_RU", &status);
    if (U_FAILURE(status))
        return 0;
    ucol_close(collator);
    return 0;
}