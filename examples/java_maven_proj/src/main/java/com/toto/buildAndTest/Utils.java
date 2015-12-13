package com.toto.buildAndTest;

import java.util.Date;
import java.util.Calendar;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public class Utils
{
  public static String getDateTime(){
    DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    Calendar cal = Calendar.getInstance();
    return (dateFormat.format(cal.getTime())); //2015/12/12 23:00:00
   }
}

