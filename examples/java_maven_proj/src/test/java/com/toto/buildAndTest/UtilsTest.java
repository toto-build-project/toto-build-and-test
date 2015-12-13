package com.toto.buildAndTest;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for Utils.
 */
public class UtilsTest 
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public UtilsTest( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( UtilsTest.class );
    }

    /**
     * the main test function for UtilsTest
     */
    public void testUtils()
    {
        //Verify getDateTime function is formatted as: 2015/12/12 23:00:00
        String datetime = Utils.getDateTime();
        assertTrue( datetime.length() == 19);
    }
}
