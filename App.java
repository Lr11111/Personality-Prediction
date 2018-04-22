package cs6120.project;

import java.io.*;
import java.util.*;
import twitter4j.*;
import twitter4j.conf.*;

/**
 * Hello world!
 *
 */
public class App 
{
	public static void main(String[] a) throws Exception{

	    ConfigurationBuilder cb = new ConfigurationBuilder();
//	    cb.setOAuthConsumerKey("bHsblsl433krl5140WSKFPiRF");
//	    cb.setOAuthConsumerSecret("WzFp3J9wPyw0FNTt8sNYXpjM1Mw2yiXLhKO0RvCbMMX4rEIfe3");
//	    cb.setOAuthAccessToken("920068723960107009-d1ppfYvxGwVWIYijvowJeRQdqzLD8KV");
//	    cb.setOAuthAccessTokenSecret("Ra4gHpRGOqlUSFOmbU91snxq4xewBzOQ09FBmOpOJ28iC");
	    cb.setOAuthConsumerKey("BNnrpyoziW66oWlvI6YeqK6NZ");
	    cb.setOAuthConsumerSecret("PPvyce4wKpZ6Sa2o2WEVhITMD6qsMyqkGNqrsfja9EMoTMqdry");
	    cb.setOAuthAccessToken("923010508692885505-cxqDB7uHzAZobOgYWRmZFsacCMlICGh");
	    cb.setOAuthAccessTokenSecret("hht4gssAvDDkKfcp1AjchvgduCi6avODaGsGPaGp5Vnjb");

	    Twitter twitter = new TwitterFactory(cb.build()).getInstance();
	    
	    File file = new File("/home/shashikirang/Downloads/Users_3.txt");
	    File fileWrite = new File("/home/shashikirang/Downloads/User_tweets_3.txt");
	    
	    BufferedReader br = new BufferedReader(new FileReader(file));
	    BufferedWriter writer = new BufferedWriter(new FileWriter(fileWrite, true));
	     
	    String line;
	    int totalTweets = 0;
	    
	    while((line = br.readLine()) != null) {
	    	long userID = Long.parseLong(line);
		    List<Status> statuses = new ArrayList();
		    try {
		    	Paging page = new Paging(1, 200);
		    	statuses.addAll(twitter.getUserTimeline(userID, page));
		    	
		    }catch (TwitterException e) {
		    	e.printStackTrace();
		    }
		    
		    for (int x=0; x<statuses.size(); x++) {
		    	writer.append(line + ":::" + statuses.get(x).getText() + "\n");
		    	totalTweets++;
		    }	    	
	    }	    
	    System.out.print(totalTweets);	    
	}
}
