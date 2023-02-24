/**
   @file NMEAsentencefunc.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief NMEA 0183 sentence functions
   @version 1.0
   @date 2022-04-02

   @copyright Copyright (c) 2022
*/

#if !defined(__NMEA_SENTENCE_FUNC_H__)
    #define __NMEA_SENTENCE_FUNC_H__
    #include <InputHandler.h>
using namespace ih;
void NMEA_0183_AAM(Input* inputProcess)
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

void NMEA_0183_APA(Input* inputProcess)
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

void NMEA_0183_APB(Input* inputProcess)
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

void NMEA_0183_BOD(Input* inputProcess)
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

void NMEA_0183_BWC(Input* inputProcess)
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

void NMEA_0183_BWR(Input* inputProcess)
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

void NMEA_0183_DBT(Input* inputProcess)
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

void NMEA_0183_DPT(Input* inputProcess)
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

void NMEA_0183_GGA(Input* inputProcess)
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

void NMEA_0183_GLL(Input* inputProcess)
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

void NMEA_0183_GSA(Input* inputProcess)
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

void NMEA_0183_GSV(Input* inputProcess)
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

void NMEA_0183_HDM(Input* inputProcess)
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

void NMEA_0183_HDT(Input* inputProcess)
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

void NMEA_0183_HSC(Input* inputProcess)
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

void NMEA_0183_MTW(Input* inputProcess)
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

void NMEA_0183_RMB(Input* inputProcess)
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

void NMEA_0183_RMC(Input* inputProcess)
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

void NMEA_0183_VTG(Input* inputProcess)
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

void NMEA_0183_WCV(Input* inputProcess)
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

void NMEA_0183_WPL(Input* inputProcess)
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

void NMEA_0183_XTE(Input* inputProcess)
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

void NMEA_0183_XTR(Input* inputProcess)
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
