
# Toto Project: Verification of Build and Test Phase


### I. Execution through Toto Project Build/Test Verification

![](https://cloud.githubusercontent.com/assets/14291263/11646270/44d84422-9d2a-11e5-95d4-a17cf60a9076.png)



### II. Toto’s Purpose
Toto aims to improve the security of the entire software development process by recording and verifying the metadata produced throughout the process. We are designing a tool with the goal of making it easier to verify that the build was executed securely and that appropriate testing was performed. This would help to assure an end user that the code can be trusted and might improve the ease of detection of compromised build systems, such as the hack on Apple’s Xcode[1].  
The build of a piece of software will generate output and/or log data containing details of the build process, which our tool will capture for the end-user. A similar process will be implemented for testing, capturing the relevant details for each test that is run. In all cases, the information our tool captures will be converted to specific metadata canonical JSON format and written to a file. 


### III. Verification of Build
Information about a piece of software’s build process can strongly influence the end-user’s faith in the software’s reliability and authenticity. As such, our tool will provide signed metadata files (in the JSON format similar to that of the TUF project) detailing certain key points of information. Our tool will parse the specification files (e.g. makefile) of common build systems, like Maven or Make, as well as the build output, and extract relevant information, such as a build timestamp, version information, programming language, compiler, as well as build environment details (e.g. host operating system). This parsed information will then be passed to our central module (main.py) which will generate and sign a JSON file in the appropriate format.

### IV. Verification of Test
Capturing test results is critical to the development process. The output from tests confirms an application’s expected behavior with actual behavior. This portion of our framework focuses on consolidating data from application tests and describing the results in JSON format. Similar to the build process, our tool will parse the output of the tests performed and pass the pertinent details to the central module to produce and sign the JSON file. Producing this metadata attests that the software has been through the testing cycle with the specified software, allowing a baseline of the successes and failures to be recorded.
If the end-user finds that the testing verification baseline has changed to skew towards failures, or that certain tests were not even performed, he/she may consider this software version to be potentially unstable or untrusted and he/she may decide to pass over this version and to wait for a different release of the software.


### V. Signing Architecture
For the architecture of the metadata signatures, we decided to use the TUF libraries.  Currently, TUF provides modules that support the signing of metadata such as generating keys, creating signatures and verifying signatures.  The Toto signing architecture will support signing with keys based on RSA256. For simplicity, we will not use the signature roles that TUF uses. 


### VI. Threat Modeling
**Problem:** How do we make sure that the necessary build constraints and tests are enforced?
**Solution:** A policy file is included that will contain all the constraints that need to be met in order for the build or tests to pass. See section X. Policy File for more information.

**Problem:** How will the end user know whether the software has been tested sufficiently?
**Solution:** The metadata generated for the build or tests of the software will aggregate the number of successes, failures, and warnings that were produced during the building or testing of the software. The user can then determine based on these statistics whether or not the software is safe to use.

**Problem:** How do we make sure that the metadata is not falsified by a malicious attacker?
**Solution:** All of the metadata that is generated will be signed with the signatures included into the metadata file. The Toto framework can then verify if the signatures are valid for the metadata. See section V. Signing Architecture for more information.

**Problem:** How will we make sure that the metadata is signed by a trusted organization? <br>
**Possible Solution:** A public key infrastructure can be implemented in which Toto will act as a validation authority. Toto will maintain a storage of key ids along with public keys for different trusted organizations. A possible solution for storage could be an online database. Each organization that wants to be publicly verifiable will have to have their keys registered with Toto. To sign metadata, the organization that is running the build or the tests will sign the metadata with their own private key. To verify the metadata publicly, Toto will check if the key id and public key is contained in its storage of keys as well as verifying the metadata and signature using the public key. This solution is currently not implemented in Toto but it may be integrated in the future along with the other phases within the Toto framework. 

### VII. Setup Instructions
* Setup by running:  "python setup.py install" and "pip install -r requirements.txt" <br>
* See an example metadata generation by running:  ./runme


### VIII. Project Structure
The files are structured as: <br>
* \<base_dir\> - main code files are located in the base directory <br>
* \<base_dir\>/examples - sample example cases for project execution <br>
* default_policy.json - contains the project’s default policy <br>
* metadata.json - contains the generated json from build/test


### IX. Toto Usage
In order to use Toto, the policy file needs to be configured. See section X. Policy File for more information regarding configuring it. If there are no particular constraints, the default policy file can be used out of the box. To run Toto, simply run the program using python while passing in a string as an argument that would contain the shell command used to either build or test your software. 

###### For example:
python main.py “[command goes here]” --input [file passed to command] --policy [alternate policy file] <br>
* Sample C example:  python main.py "cd examples/c_code_proj; ./makefile" 

###### Arguments:  
* command - Mandatory field.  Argument contains executing command <br>
* input - Optional field.  Argument is passed to the command for execution <br>
* policy - Optional field.  Default is “default_policy.json”, otherwise alternate policy specified here 

###### Output Files:  
* out - all stdout generated <br>
* err - all stderr generated <br>
* metadata.json - contains the generated json from build/test <br>


### X. Policy File
The policy file enables an organization to specify the constraints for the type of configuration and parameters that need to be in place for its software builds and tests. In addition, keywords for the parser to determine success, failure, and warnings can be specified so that they are more catered to the specific build or test that is being run. The policy file is in JSON format. If a constraint is not applicable then it is assigned null, otherwise, the expected value for the constraint is included. The default format for the policy file is shown below:
```
{     
   "constraints": {         
      "return_code": null,         
      "command_flags": [],         
      "cpu_arch": null,         
      "os": {             
         "kernel": null,             
         "release": null,             
         "version": null         
      }     
   },     
   "supplied_data": {         
      "software_version": null,         
      "word_lists": {             
         "success": ["success", "succeed", "succeeded", "successfully", "installed", "finished", "pass", "passed"],             
         "failure": ["fail", "failed", "failure", "error", "fault"],             
         "warning": ["warn", "warning", "alert", "caution"]         
      }     
   }
}
```



***

#### References:
[1]http://researchcenter.paloaltonetworks.com/2015/09/novel-malware-xcodeghost-modifies-xcode-infects-apple-ios-apps-and-hits-app-store/
