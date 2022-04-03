#if !defined(__NMEA_SENTENCE_FUNC__)
#define __NMEA_SENTENCE_FUNC__
#include <InputHandler.h>

void NMEA_0183_AAM(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse AAM fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse AAM fields"));
}

void NMEA_0183_APA(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse APA fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse APA fields"));
}

void NMEA_0183_APB(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse APB fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse APB fields"));
}

void NMEA_0183_BOD(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse BOD fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse BOD fields"));    
}

void NMEA_0183_BWC(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse BWC fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse BWC fields"));
}

void NMEA_0183_BWR(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse BWR fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse BWR fields"));
}

void NMEA_0183_DBT(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse DBT fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse DBT fields"));
}

void NMEA_0183_DPT(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse DPT fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse DPT fields"));
}

void NMEA_0183_GGA(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse GGA fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse GGA fields"));
}

void NMEA_0183_GLL(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse GLL fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse GLL fields"));
}

void NMEA_0183_GSA(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse GSA fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse GSA fields"));
}

void NMEA_0183_GSV(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse GSV fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse GSV fields"));
}

void NMEA_0183_HDM(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse HDM fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse HDM fields"));
}

void NMEA_0183_HDT(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse HDT fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse HDT fields"));
}

void NMEA_0183_HSC(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse HSC fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse HSC fields"));
}

void NMEA_0183_MTW(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse MTW fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse MTW fields"));
}

void NMEA_0183_RMB(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse RMB fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse RMB fields"));
}

void NMEA_0183_RMC(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse RMC fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse RMC fields"));
}

void NMEA_0183_VTG(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse VTG fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse VTG fields"));
}

void NMEA_0183_WCV(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse WCV fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse WCV fields"));
}

void NMEA_0183_WPL(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse WPL fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse WPL fields"));
}

void NMEA_0183_XTE(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse XTE fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse XTE fields"));
}

void NMEA_0183_XTR(UserInput* inputProcess)
{
    Serial.println(F("NMEA parse XTR fields"));
    char* ptr = inputProcess->nextArgument();
    size_t idx = 0;
    while (ptr != NULL)
    {
        Serial.print(idx);
        Serial.print(F(" "));
        Serial.println(ptr);
        ptr = inputProcess->nextArgument();
        idx++;
    }
    Serial.println(F("end NMEA parse XTR fields"));
}

#endif