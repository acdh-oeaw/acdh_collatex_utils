<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="1.0">
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="tei:app">
        <xsl:copy>
            <xsl:apply-templates select="tei:lem"/>
            <xsl:for-each select="./tei:rdg[contains(@wit, '!!!REPLACEME!!!')]">
                <lem xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:attribute name="wit">
                        <xsl:value-of select="@wit"/>
                    </xsl:attribute>
                    <xsl:value-of select="./text()"/>
                </lem>
            </xsl:for-each>
            <xsl:for-each select="./tei:rdg[not(contains(@wit, '!!!REPLACEME!!!'))]">
                <rdg xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:attribute name="wit">
                        <xsl:value-of select="@wit"/>
                    </xsl:attribute>
                    <xsl:value-of select="./text()"/>
                </rdg>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>