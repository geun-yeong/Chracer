# *Chracer*

*Chracer* is a proof-of-concept tool. *Chracer* uses object layout information obtained from the PDB to extract forensically meaningful information from Chromium's virtual memory. **Because *Chracer* is not yet optimized, some code is hard-coded.**

# Dataset

## Minidumps

The Google Driver link that shares minidumps corresponding to experiment cases
> https://drive.google.com/drive/folders/11rEJ41PsUZBDKKhDYjrpVotb0qU7vomk?usp=sharing

## Symbols

Thie Mega links that share parsed symbol files of _chrome.dll_ and _content.dll_ of Chromium (version 113.0.5650.0, commit fed2d65)
> https://1drv.ms/u/s!AqpVJMlnbz-NgehgIjEQxAn2Pybdew?e=ef2lim
> https://1drv.ms/u/s!AqpVJMlnbz-Ngehf5xHmyo8iy52eqw?e=Ek9RAn

# Scenario

Note: all timestamps are written as UTC+0.

## Case1

1. [2023-03-20 02:03:22] 1st window was created
1. [2023-03-20 02:03:36] 2nd window was created
1. [2023-03-20 02:03:37] 3rd window was created
1. [2023-03-20 02:03:38] 4th window was created
1. [2023-03-20 02:03:46] Having visited "https://www.google.com/" from "chrome://newtab" on 1st window
1. [2023-03-20 02:04:07] Having visited "https://github.com/" from "chrome://newtab" on 2nd window
1. [2023-03-20 02:04:07] Having visited "https://www.youtube.com/" from "chrome://newtab" on 3rd window
1. [2023-03-20 02:04:11] Having visited "https://www.chromium.org/" from "chrome://newtab" on 4th window

## Case2

1. [2023-03-14 05:16:29] Window and default tab were created
1. [2023-03-14 05:16:33] 2nd tab was created
1. [2023-03-14 05:16:35] 3rd tab was created
1. [2023-03-14 05:16:36] 4th tab was created
1. [2023-03-14 05:16:37] 5th tab was created
1. [2023-03-14 05:16:38] 6th tab was created
1. [2023-03-14 05:16:39] 7th tab was created
1. [2023-03-14 05:16:40] 8th tab was created
1. [2023-03-14 05:17:##] 1st tab group was created and set its name as "TabGroup1" and theme color as yellow
1. [2023-03-14 05:17:##] default and 2nd tabs were set into 1st tab group
1. [2023-03-14 05:17:##] 2nd tab group was created and set its name as "TabGroup2" and theme color as red
1. [2023-03-14 05:17:##] 3rd and 4th tabs were set into 1st tab group
1. [2023-03-14 05:17:##] 3rd tab group was created and set its name as "TabGroup3" and theme color as grey
1. [2023-03-14 05:17:##] 5th and 6th tabs were set into 1st tab group
1. [2023-03-14 05:17:##] 4th tab group was created and set its name as "TabGroup4" and theme color as blue
1. [2023-03-14 05:17:##] 7th and 8th tabs were set into 1st tab group

## Case3

1. [2023-03-14 07:45:04] Window and default tab were created
1. [2023-03-14 07:45:28] 2nd tab was created
1. [2023-03-14 07:45:53] Having visited "https://www.wikipedia.org/" from "chrome://newtab" on 1st tab
1. [2023-03-14 07:46:02] Having visited "https://en.wikipedia.org/wiki/Digital_forensics" from "https://www.wikipedia.org/" on 1st tab
1. [2023-03-14 07:46:44] Having visited "https://en.wikipedia.org/wiki/Computer_forensics" from "https://en.wikipedia.org/wiki/Digital_forensics" on 1st tab
1. [2023-03-14 07:46:57] Having visited "https://en.wikipedia.org/wiki/Digital_evidence" from "https://en.wikipedia.org/wiki/Computer_forensics" on 1st tab
1. [2023-03-14 07:47:11] Having visited "https://en.wikipedia.org/wiki/Best_evidence_rule" from "https://en.wikipedia.org/wiki/Digital_evidence" on 1st tab
1. [2023-03-14 07:56:37] Having visited "https://www.chromium.org/" from "chrome://newtab" on 2nd tab
1. [2023-03-14 07:56:41] Having visited "https://www.chromium.org/Home" from "https://www.chromium.org/" on 2nd tab
1. [2023-03-14 07:59:36] Having visited "https://www.chromium.org/developers" from "https://www.chromium.org/Home" on 2nd tab
1. [2023-03-14 07:59:37] Having visited "https://www.chromium.org/developers/how-tos/getting-around-the-chrome-source-code" from "https://www.chromium.org/developers" on 2nd tab
1. [2023-03-14 08:00:04] Having visited "https://www.chromium.org/developers/design-documents/multi-process-architecture" from "https://www.chromium.org/developers/how-tos/getting-around-the-chrome-source-code" on 2nd tab

## Case4

Note: extracting SSL certificate information from case 3 dump file.

## Case5

1. [2023-03-14 10:36:25] 1st normal window was created
1. [2023-03-14 10:36:29] 2nd normal window was created
1. [2023-03-14 10:36:32] 1st private window was created
1. [2023-03-14 10:36:34] 2nd window was created
1. [2023-03-14 10:36:44] Having visited "https://www.google.com/" from "chrome://newtab" on 1st normal window
1. [2023-03-14 10:36:48] Having visited "https://www.youtube.com/" from "chrome://newtab" on 2nd normal window
1. [2023-03-14 10:36:53] Having visited "https://www.chromium.org/" from "chrome://newtab" on 1st private window
1. [2023-03-14 10:36:57] Having visited "https://www.wikipedia.org/" from "chrome://newtab" on 2nd private window

## Google Chrome

1. [2023-03-18 10:10:32] Window and default tab were created
1. [2023-03-18 10:10:47] Having visited "https://www.wikipedia.org/" from "chrome://new-tab-page"
1. [2023-03-18 10:10:53] Having visited "https://en.wikipedia.org/wiki/Digital_forensics" from "https://www.wikipedia.org/"
1. [2023-03-18 10:11:01] Having visited "https://en.wikipedia.org/wiki/Cybercrime" from "https://en.wikipedia.org/wiki/Digital_forensics"
1. [2023-03-18 10:11:22] Having visited "https://en.wikipedia.org/wiki/Cyberwarfare" from "https://en.wikipedia.org/wiki/Cybercrime"
1. [2023-03-18 10:11:33] Having visited "https://en.wikipedia.org/wiki/Cyberattack" from "https://en.wikipedia.org/wiki/Cyberwarfare"

## Microsoft Edge

1. [2023-03-18 10:15:11] Window and default tab were created
1. [2023-03-18 10:15:17] Having visited "https://www.wikipedia.org/" from "https://ntp.msn.com/edge/ntp?..."
1. [2023-03-18 10:15:21] Having visited "https://en.wikipedia.org/wiki/Digital_forensics" from "https://www.wikipedia.org/"
1. [2023-03-18 10:15:31] Having visited "https://en.wikipedia.org/wiki/IoT_Forensics" from "https://en.wikipedia.org/wiki/Digital_forensics"
1. [2023-03-18 10:15:45] Having visited "https://en.wikipedia.org/wiki/Memory_forensics" from "https://en.wikipedia.org/wiki/IoT_Forensics"
1. [2023-03-18 10:16:03] Having visited "https://en.wikipedia.org/wiki/Volatility_(software)" from "https://en.wikipedia.org/wiki/Memory_forensics"

## Brave

1. [2023-07-02 06:50:09] Window and default tab were created
1. [2023-07-02 06:50:26] Having visited "https://www.wikipedia.org/" from "chrome://newtab"
1. [2023-07-02 06:50:43] Having visited "https://en.wikipedia.org/wiki/Digital_forensics" from "https://www.wikipedia.org/"
1. [2023-07-02 06:59:09] Having visited "https://en.wikipedia.org/wiki/Network_forensics" from "https://en.wikipedia.org/wiki/Digital_forensics"
1. [2023-07-02 07:06:26] Having visited "https://en.wikipedia.org/wiki/Transport_Layer_Security" from "https://en.wikipedia.org/wiki/Network_forensics"
1. [2023-07-02 07:11:13] Having visited "https://en.wikipedia.org/wiki/HTTPS" from "https://en.wikipedia.org/wiki/Transport_Layer_Security"

# Usage

We developed the tools based on Python 3.7.9.

## Setup

In Linux:
```
$ git clone https://github.com/chracer/Chracer.git
$ cd Chracer
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

In Windows:
```
> git clone https://github.com/chracer/Chracer.git
> cd Chracer
> python -m venv venv
> venv\Scripts\activate
(venv) > pip install -r requirements.txt
```

## Download datasets

1. Storing minidumps files to _dumps_ directory after downloading them
2. Sotring parsed symbol files to _symbols_ directory after downloading them
3. After completing the download, it should have a folder tree like the one below
    ```
    Chracer/
    +  chracer/
    |  +  ...
    +  dumps/
    |  +  case_google_chrome.dmp
    |  +  case_microsoft_edge.dmp
    |  +  case_brave.dmp
    |  +  case1.dmp
    |  +  case2.dmp
    |  +  case3.dmp
    |  +  case4.dmp
    |  +  case5.dmp
    +  symbols/
    |  +  chrome.dll.pdb.xml
    |  +  content.dll.pdb.xml
    +  case1.py
    +  case2.py
    +  case3.py
    +  case4.py
    +  case5.py
    +  finder.py
    +  case_google_chrome.py
    +  case_microsoft_edge.py
    +  case_brave.py
    +  README.md
    +  requirements.txt
    ```

## Case 1

In this case, the tool extracts session id of each _Browser_ object, tab, document title, URL from _dumps/case1.dmp_. 

```
(venv) $ python3 case1.py
```

## Case 2

In this case, the tool extracts tab group-related information from _dumps/case2.dmp_.

```
(venv) $ python3 case2.py
```

## Case 3

In this case, the tool extracts visited URL-related information from _dumps/case3.dmp_.

```
(venv) $ python3 case3.py
```

## Case 4

In this case, the tool extracts SSL certificate-related information from _dumps/case4.dmp_ (this file is same to _dumps/case3.dmp_).

```
(venv) $ python3 case4.py
```

## Case 5

In this case, the tool extracts visited URL and distinguishes whether discovered _Browser_ object is a private mode or not.

```
(venv) $ python3 case5.py
```

## Case Google Chrome

In this case, the tool extracts visited URL-related information from _dumps/case\_google\_chrome.dmp_ by adjusting offset of fields of some classes.

```
(venv) $ python3 case_google_chrome.py
```

## Case Microsoft Edge

In this case, the tool extracts visited URL-related information from _dumps/case\_microsoft\_edge.dmp_ by adjusting offset of fields of some classes.

```
(venv) $ python3 case_microsoft_edge.py
```

## Case Brave

In this case, the tool extracts visited URL-related information from _dumps/case\_brave.dmp_ by adjusting offset of fields of some classes.

```
(venv) $ python3 case_brave.py
```

## Finder

This code takes a minidump file as input. After it discovers a _Browser_ object from virtual memory dumped in minidump, it extracts visited URL-related information.

```
(venv) $ python3 finder.py dumps/case1.dmp
```

# Notes

System requirements
- 32GB of RAM
- At least 50GB of free disk space
