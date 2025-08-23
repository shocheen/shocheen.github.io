import re
import pandas as pd
import os

# Content scraped from the website
website_content = """
    ____________________
   Search this site
   Embedded Files
   (BUTTON)
   Skip to main content
   (BUTTON)
   Skip to navigation
   [1]Sachin Kumar
     * [2]Home
     * [3]Teaching
     * [4]My Group
     * [5]Prospective Students
     * [6]Research
     * [7]Vitae

   [8]Sachin Kumar
     * [9]Home
     * [10]Teaching
     * [11]My Group
     * [12]Prospective Students
     * [13]Research
     * [14]Vitae
     * More
          + [15]Home
          + [16]Teaching
          + [17]My Group
          + [18]Prospective Students
          + [19]Research
          + [20]Vitae

Publications

     * [2025][[21]pdf][[22]code][[23]data] Orevaoghene Ahia, Martijn
       Bartelds, Kabir Ahuja, Hila Gonen, Valentin Hofmann, Siddhant
       Arora, Shuyue Stella Li, Vishal Puttagunta, Mofetoluwa Adeyemi,
       Charishma Buchireddy, Ben Walls, Noah Bennett, Shinji Watanabe,
       Noah A. Smith, Yulia Tsvetkov, Sachin Kumar, "BLAB: Brutally Long
       Audio Bench", preprint.
     * [2025][[24]pdf] Zhouhang Xie, Junda Wu, Yiran Shen, Yu Xia, Xintong
       Li, Aaron Chang, Ryan Rossi, Sachin Kumar, Bodhisattwa Prasad
       Majumder, Jingbo Shang, Prithviraj Ammanabrolu, Julian McAuley, "A
       Survey on Personalized and Pluralistic Preference Alignment in
       Large Language Models", preprint.
     * [2025][[25]pdf][[26]code] Abraham Toluwase Owodunni, Orevaoghene
       Ahia, Sachin Kumar, "FLEXITOKENS: Flexible Tokenization for
       Evolving Language Models", preprint, also presented at Tokenization
       Workshop @ICML 2025.
     * [2025][pdf] Carolina Hatanpää, Noah A. Smith, Sachin Kumar, "On
       Distributional Robustness of In-Context Learning for Text
       Classification", Second Workshop on Test-Time Adaptation: Putting
       Updates to the Test! @ICML 2025.
     * [2025][[27]pdf][[28]code] Patrick Queiroz Da Silva, Hari
       Sethuraman, Dheeraj Rajagopal, Hannaneh Hajishirzi, Sachin Kumar,
       "Steering off Course: Reliability Challenges in Steering Language
       Models", 2025 Conference of the Association for Computational
       Linguistics (ACL 2025). Oral (top 8%), Panel (top 0.8%).
     * [2025][[29]pdf][[30]code][[31]demo] Jaesung Tae, Hamish Ivison,
       Sachin Kumar, Arman Cohan, "TESS 2: A Large-Scale Generalist
       Diffusion Language Model", 2025 Conference of the Association for
       Computational Linguistics (ACL 2025) Oral (top 8%).
     * [2025][[32]pdf][[33]code][[34]data][[35]blog] Lester James V.
       Miranda, Yizhong Wang, Yanai Elazar, Sachin Kumar, Valentina
       Pyatkin, Faeze Brahman, Noah A. Smith, Hannaneh Hajishirzi, Pradeep
       Dasigi, "Hybrid Preferences: Learning to Route Instances for Human
       vs. AI Feedback", 2025 Conference of the Association for
       Computational Linguistics (ACL 2025).
     * [2025][[36]pdf][[37]code and data] Harsh Kohli, Sachin Kumar, Huan
       Sun, "GroundCocoa: A Benchmark for Evaluating Compositional &
       Conditional Reasoning in Language Models", 2025 Annual Conference
       of the Nations of the Americas Chapter of the Association for
       Computational Linguistics (NAACL 2025).
     * [2025][[38]pdf][[39]code][[40]data] Sachin Kumar*, Chan Young
       Park*, Yulia Tsvetkov, Noah A. Smith, Hannaneh Hajishirzi, "ComPO:
       Community Preferences for Language Model Personalization", 2025
       Annual Conference of the Nations of the Americas Chapter of the
       Association for Computational Linguistics (NAACL 2025).
     * [2025][[41]pdf][[42]code][[43]leaderboard] Nathan Lambert,
       Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin,
       Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi,
       Noah A. Smith, Hannaneh Hajishirzi, "RewardBench: Evaluating Reward
       Models for Language Modeling", 2025 Annual Conference of the
       Nations of the Americas Chapter of the Association for
       Computational Linguistics (NAACL 2025) Findings.
     * [2024][[44]pdf][[45]code][[46]data][[47]blog] Faeze Brahman*,
       Sachin Kumar*, Vidhisha Balachandran, Pradeep Dasigi, Valentina
       Pyatkin, Abhilasha Ravichander, Sarah Wiegreffe, Nouha Dziri,
       Khyathi Chandu, Jack Hessel, Yulia Tsvetkov, Noah A. Smith, Yejin
       Choi, Hannaneh Hajishirzi, "The Art of Saying No: Contextual
       Noncompliance in Language Models", Thirty-eighth Conference on
       Neural Information Processing Systems (NeurIPS) 2024: Datasets and
       Benchmarks.
     * [2024][[48]pdf][code] Orevaoghene Ahia, Sachin Kumar, Hila Gonen,
       Valentin Hoffman, Tomasz Limisiewicz, Yulia Tsvetkov, Noah A.
       Smith, "MAGNET: Improving the Multilingual Fairness of Language
       Models with Adaptive Gradient-Based Tokenization", Thirty-eighth
       Conference on Neural Information Processing Systems (NeurIPS) 2024.
     * [2024][[49]pdf][code] Liwei Jiang, Kavel Rao, Seungju Han, Allyson
       Ettinger, Faeze Brahman, Sachin Kumar, Niloofar Mireshghallah,
       Ximing Lu, Maarten Sap, Yejin Choi, Nouha Dziri, "WildTeaming at
       Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer
       Language Models", Thirty-eighth Conference on Neural Information
       Processing Systems (NeurIPS) 2024.

     * [2024][[50]pdf][code] Luca Soldaini, Rodney Kinney, Akshita Bhagia,
       Dustin Schwenk, David Atkinson, Russell Authur, Ben Bogin, Khyathi
       Chandu, Jennifer Dumas, Yanai Elazar, Valentin Hofmann, Ananya
       Harsh Jha, Sachin Kumar, Li Lucy, Xinxi Lyu, Nathan Lambert, Ian
       Magnusson, Jacob Morrison, Niklas Muennighoff, Aakanksha Naik,
       Crystal Nam, Matthew E. Peters, Abhilasha Ravichander, Kyle
       Richardson, Zejiang Shen, Emma Strubell, Nishant Subramani, Oyvind
       Tafjord, Pete Walsh, Luke Zettlemoyer, Noah A. Smith, Hannaneh
       Hajishirzi, Iz Beltagy, Dirk Groeneveld, Jesse Dodge, Kyle Lo,
       "Dolma: an Open Corpus of Three Trillion Tokens for Language Model
       Pretraining Research", 2024 Conference of the Association for
       Computational Linguistics (ACL 2024). Best Resource Paper Award.
     * [2024][[51]pdf][code] YuHan Liu, Shangbin Feng, Xiaochuang Han,
       Vidhisha Balachandran, Chan Young Park, Sachin Kumar, Yulia
       Tsvetkov, "What Constitutes a Faithful Summary? Preserving Author
       Perspectives in News Summarization", 2024 Conference of the North
       American Chapter of the Association for Computational Linguistics
       (NAACL 2024).
     * [2024][[52]pdf][code] Xiaochuang Han, Sachin Kumar, Yulia Tsvetkov,
       Marjan Ghazvininejad, "SSD-2: Scaling and Inference-time Fusion of
       Diffusion Language Models", 2024 Conference of the North American
       Chapter of the Association for Computational Linguistics (NAACL
       2024).
     * [2024][[53]pdf][[54]code]  Sachin Kumar, Chan Young Park, Yulia
       Tsvetkov, "Gen-Z: Generative Zero-Shot Text Classification with
       Contextualized Label Descriptions", International Conference on
       Learning Representations (ICLR 2024).
     * [2023][[55]pdf][code] Orevaoghene Ahia, Sachin Kumar, Hila Gonen,
       Jungo Kasai, David R. Mortensen, Noah A. Smith, Yulia Tsvetkov, "Do
       All Languages Cost the Same? Tokenization in the Era of Commercial
       Language Models", 2023 Conference on Empirical Methods in Natural
       Language Processing (EMNLP 2023).
     * [2023][[56]pdf][code] Melanie Sclar, Sachin Kumar, Peter West,
       Alane Suhr, Yejin Choi and Yulia Tsvetkov, “Minding Language
       Models’ Theory of Mind: A Plug-and-Play Multi-Character Belief
       Tracker”, 2023 Conference of the Association for Computational
       Linguistics (ACL 2023). Outstanding Paper Award
     * [2023] [[57]pdf] [code] Tianxing He, Jingyu Zhang, Tianle Wang,
       Sachin Kumar, Kyunghyun Cho, James Glass, Yulia Tsvetkov, "On the
       Blind Spots of Model-Based Evaluation Metrics for Text Generation",
       2023 Conference of the Association for Computational Linguistics
       (ACL 2023).
     * [2023] [[58]pdf] [[59]code][[60]demo] Xiaochuang Han, Sachin Kumar,
       Yulia Tsvetkov, "SSD-LM: Semi-autoregressive Simplex-based
       Diffusion Language Model for Text Generation and Modular Control",
       2023 Conference of the Association for Computational Linguistics
       (ACL 2023).
     * [2023][pdf] Leon Derczynski, Hannah Rose Kirk, Vidhisha
       Balachandran, Sachin Kumar, Yulia Tsvetkov, M. R. Leiser, Saif
       Mohammad, "Assessing Language Model Deployment with Risk Cards",
       preprint.
     * [2023] [[61]pdf] Sachin Kumar*, Vidhisha Balachandran*, Lucille
       Njoo, Antonios Anastasopoulos, Yulia Tsvetkov, "Language Generation
       Models Can Cause Harm: So What Can We Do About It? An Actionable
       Survey", 2023 Conference of the European Chapter of the Association
       for Computational Linguistics (EACL 2023).
     * [2022] [[62]pdf] [[63]code] Melanie Sclar, Peter West, Sachin
       Kumar, Yulia Tsvetkov and Yejin Choi, “Reference-Free Sentence
       Summarization with Sharper Controllability through Symbolic
       Knowledge Distillation”, 2022 Conference on Empirical Methods in
       Natural Language Processing (EMNLP 2022).
     * [2022] [[64]pdf][[65]code] Sachin Kumar, Biswajit Paria, Yulia
       Tsvetkov, “Gradient-based Constrained Sampling from Language
       Models”, 2022 Conference on Empirical Methods in Natural Language
       Processing (EMNLP 2022).
     * [2021] [[66]pdf][[67]code] Sachin Kumar, Eric Malmi, Aliaksei
       Severyn, Yulia Tsvetkov. Controlled Text Generation as Continuous
       Optimization with Multiple Constraints. Thirty-Fifth Conference on
       Neural Information Processing Systems (NeurIPS) 2021.
     * [2021] [pdf] [code] Monisha Jegadeesan, Sachin Kumar, John Wieting,
       Yulia Tsvetkov. Improving the Diversity of Unsupervised
       Paraphrasing with Embedding Outputs. Multilingual Representation
       Learning Workshop at EMNLP 2021.
     * [2021] [[68]pdf] [[69]code] Sachin Kumar, Antonios Anastasopoulos,
       Shuly Wintner, Yulia Tsvetkov. Machine Translation into
       Low-Resource Language Varieties. In the proceedings of 2021
       Conference on Association of Computational Linguistics (ACL).
     * [2021] [[70]pdf] Lidia Kidane, Sachin Kumar, Yulia Tsvetkov. An
       Exploration of Data Augmentation Techniques for Improving English
       to Tigrinya Translation. The 2nd AfricaNLP Workshop at EACL 2021.
     * [2020] [[71]pdf] Zi-Yi Dou, Sachin Kumar, Yulia Tsvetkov, A Deep
       Reinforced Model for Zero-Shot Cross-Lingual Summarization with
       Bilingual Semantic Similarity Rewards. The 4th Workshop on Neural
       Generation and Translation (ACL) 2020
     * [2019] [[72]pdf] Gayatri Bhat, Sachin Kumar, Yulia Tsvetkov, A
       Margin-based Loss with Synthetic Negative Samples for
       Continuous-output Machine Translation, The 3rd Workshop on Neural
       Generation and Translation (EMNLP) 2019
     * [2019] [[73]pdf][[74]code] Sachin Kumar, Shuly Wintner, Noah A.
       Smith, Yulia Tsvetkov, Topics to Avoid: Demoting Latent Confounds
       in Text Classification, 2019 Conference on Empirical Methods in
       Natural Language Processing (EMNLP) 2019
     * [2018] [[75]pdf] [[76]code] Sachin Kumar & Yulia Tsvetkov, Von
       Mises-Fisher Loss for Training Sequence to Sequence Models with
       Continuous Outputs, 7th International Conference on Learning
       Representations (ICLR) 2019.
     * [2018] [[77]pdf] Shreshtha Mundra*, Sachin Kumar*, Manjira Sinha,
       Sandya Mannarswamy, Mining & Summarizing E-petitions for Enhanced
       Understanding of Public Opinion, In Proceedings of the
       International Conference on Information and Knowledge Management
       (CIKM) 2018.
     * [2018] Sachin Kumar, Yulia Tsvetkov, Machine Translation with
       Continuous Outputs, ICML 2018 workshop on Theoretical Foundations
       and Applications of Deep Generative Models.
     * [2017] [[78]pdf] Sachin Kumar, Soumen Chakrabarti, Shourya Roy.
       Earth Mover Distance Pooling over Siamese LSTMs for Automatic Short
       Answer Grading. In Proceedings of the 26th International Joint
       Conference on Artificial Intelligence (IJCAI) 2017.
     * [2014] [[79]pdf] Sachin Kumar, Vikas C. Raykar, and Priyanka
       Agrawal. Decisions under drift: Adapting binary decision thresholds
       to drifts in test distribution. In Proceedings of the 6th IBM
       Collaborative Academia Research Exchange Conference. ACM, New York,
       NY, USA, Article 17, 4 pages.
       DOI=http://dx.doi.org/10.1145/2662117.2662134

   Google Sites
   Report abuse
   Google Sites
   Report abuse

References

   1. https://sites.google.com/view/sachinkumar/home
   2. https://sites.google.com/view/sachinkumar/home
   3. https://sites.google.com/view/sachinkumar/teaching
   4. https://sites.google.com/view/sachinkumar/my-group
   5. https://sites.google.com/view/sachinkumar/prospective-students
   6. https://sites.google.com/view/sachinkumar/research
   7. https://sites.google.com/view/sachinkumar/vitae
   8. https://sites.google.com/view/sachinkumar/home
   9. https://sites.google.com/view/sachinkumar/home
  10. https://sites.google.com/view/sachinkumar/teaching
  11. https://sites.google.com/view/sachinkumar/my-group
  12. https://sites.google.com/view/sachinkumar/prospective-students
  13. https://sites.google.com/view/sachinkumar/research
  14. https://sites.google.com/view/sachinkumar/vitae
  15. https://sites.google.com/view/sachinkumar/home
  16. https://sites.google.com/view/sachinkumar/teaching
  17. https://sites.google.com/view/sachinkumar/my-group
  18. https://sites.google.com/view/sachinkumar/prospective-students
  19. https://sites.google.com/view/sachinkumar/research
  20. https://sites.google.com/view/sachinkumar/vitae
  21. https://arxiv.org/abs/2505.03054
  22. https://github.com/orevaahia/brutally_long_audio_bench
  23. https://huggingface.co/datasets/oreva/blab_long_audio
  24. https://arxiv.org/abs/2504.07070
  25. https://arxiv.org/abs/2507.12720
  26. https://github.com/owos/flexitokens
  27. https://arxiv.org/abs/2504.04635
  28. https://github.com/patqdasilva/steering-off-course
  29. https://arxiv.org/abs/2502.13917
  30. https://github.com/hamishivi/tess-2
  31. https://t.co/9uRf1qx0RE
  32. https://arxiv.org/abs/2410.19133
  33. https://github.com/allenai/hybrid-preferences
  34. https://huggingface.co/datasets/allenai/multipref
  35. https://allenai.org/blog/hybrid-preferences
  36. https://arxiv.org/pdf/2404.04237
  37. https://osu-nlp-group.github.io/GroundCocoa/
  38. https://arxiv.org/abs/2410.16027
  39. https://github.com/allenai/compred
  40. https://huggingface.co/datasets/allenai/compred
  41. https://arxiv.org/abs/2403.13787
  42. https://github.com/allenai/reward-bench
  43. https://huggingface.co/spaces/allenai/reward-bench
  44. https://www.arxiv.org/abs/2407.12043
  45. https://github.com/allenai/noncompliance
  46. https://huggingface.co/datasets/allenai/coconot
  47. https://blog.allenai.org/broadening-the-scope-of-noncompliance-when-and-how-ai-models-should-not-comply-with-user-requests-18b028c5b538
  48. https://arxiv.org/abs/2407.08818
  49. https://arxiv.org/abs/2406.18510
  50. https://arxiv.org/abs/2402.00159
  51. https://arxiv.org/pdf/2311.09741v1.pdf
  52. https://arxiv.org/abs/2305.14771
  53. https://arxiv.org/pdf/2311.07115.pdf
  54. https://github.com/Sachin19/generative-classification
  55. https://arxiv.org/abs/2305.13707
  56. https://arxiv.org/abs/2306.00924
  57. https://arxiv.org/abs/2212.10020
  58. https://arxiv.org/abs/2210.17432
  59. https://github.com/xhan77/ssd-lm
  60. https://colab.research.google.com/drive/1vNKqvzzJQp3k89QPuns5ibsq-VNC9wGN?usp=sharing
  61. https://arxiv.org/abs/2210.07700
  62. https://arxiv.org/abs/2210.13800
  63. https://github.com/msclar/referee
  64. https://arxiv.org/abs/2205.12558
  65. https://github.com/Sachin19/mucoco/tree/sampling2/
  66. https://arxiv.org/abs/2108.01850
  67. https://github.com/Sachin19/mucoco
  68. https://arxiv.org/abs/2106.06797
  69. https://github.com/Sachin19/seq2seq-con
  70. https://arxiv.org/abs/2103.16789
  71. https://www.aclweb.org/anthology/2020.ngt-1.7.pdf
  72. https://www.aclweb.org/anthology/D19-5621.pdf
  73. https://arxiv.org/abs/1909.00453
  74. https://github.com/Sachin19/adversarial-classify
  75. https://openreview.net/forum?id=rJlDnoA5Y7
  76. https://github.com/Sachin19/seq2seq-con
  77. https://dl.acm.org/citation.cfm?id=3269246
  78. https://www.ijcai.org/proceedings/2017/0284.pdf
  79. http://dx.doi.org/10.1145/2662117.2662134
"""

def parse_publications(content):
    lines = content.strip().split('\n')

    # Parse references
    references = {}
    in_references_section = False
    for line in lines:
        line = line.strip()
        if line.lower() == "references":
            in_references_section = True
            continue
        if in_references_section:
            match = re.match(r'(\d+)\.\s+(.*)', line)
            if match:
                references[match.group(1)] = match.group(2)

    # Find publications section and handle multi-line entries
    pub_lines = []
    in_publications_section = False
    current_pub = ""
    for line in lines:
        line = line.strip()
        if line.lower() == "publications":
            in_publications_section = True
            continue
        if "Google Sites" in line:
            in_publications_section = False
            if current_pub:
                pub_lines.append(current_pub)
            break

        if in_publications_section:
            if line.startswith('*'):
                if current_pub:
                    pub_lines.append(current_pub)
                current_pub = line[1:].strip()
            elif current_pub: # continue of the current publication
                current_pub += " " + line

    if current_pub and current_pub not in pub_lines:
        pub_lines.append(current_pub)

    publications_data = []
    for entry in pub_lines:
        year_match = re.search(r'\[(\d{4})\]', entry)
        year = year_match.group(1) if year_match else None
        if not year:
            print(f"Skipping entry (no year found): {entry}")
            continue

        # Extract links and remove them from the entry string for easier parsing
        pdf_url, code_url = '', ''
        link_matches = re.findall(r'\[\[(\d+)\]([^\]]+)\]', entry)
        for ref_num, link_type in link_matches:
            if references.get(ref_num):
                if 'pdf' in link_type:
                    pdf_url = references[ref_num]
                elif 'code' in link_type:
                    code_url = references[ref_num]

        # Clean entry from links for easier title/author/venue parsing
        cleaned_entry = re.sub(r'\[\[\d+\].*?\]', '', entry)
        cleaned_entry = re.sub(r'\[\d{4}\]', '', cleaned_entry).strip()

        title_match = re.search(r'[\"“](.*?)[\"”]', cleaned_entry)
        if title_match:
            title = title_match.group(1)
            # Use re.split for robust splitting with different quote types
            parts = re.split(r'[\"“]' + re.escape(title) + r'[\"”]', cleaned_entry)
            authors = parts[0].strip(', ')
            venue = parts[1].strip(',. ')
        else:
            # Fallback for non-quoted titles
            parts = cleaned_entry.rsplit(', ', 1)
            if len(parts) == 2:
                text_before_venue, venue = parts

                # Now separate authors and title from text_before_venue
                # This is a heuristic. We assume the last comma separates authors and title.
                # This may not be perfect, but it's better than skipping.
                author_title_parts = text_before_venue.rsplit(', ', 1)
                if len(author_title_parts) == 2:
                    authors, title = author_title_parts
                else:
                    # If no comma, assume the whole string is the title
                    authors = ""
                    title = text_before_venue
            else:
                 print(f"Skipping entry (fallback failed to split venue): {entry}")
                 continue

        # Final cleanup
        authors = authors.strip(', ')
        venue = venue.strip(',. ')
        title = title.strip(',. ')

        # Create citation and slug
        citation = f'{authors}. ({year}). "{title}." <i>{venue}</i>.'
        url_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        publications_data.append({
            'pub_date': f'{year}-01-01',
            'title': title,
            'venue': venue,
            'excerpt': '',
            'citation': citation,
            'url_slug': url_slug,
            'paper_url': pdf_url,
            'slides_url': code_url
        })

    return publications_data

def main():
    publications = parse_publications(website_content)
    print("Parsed publications:")
    print(publications)

    if not publications:
        print("No publications were parsed. Exiting.")
        return

    df = pd.DataFrame(publications)

    # Ensure columns are in the correct order
    column_order = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url']
    # Create a new dataframe with the specified columns, filling missing ones with empty strings
    df_ordered = pd.DataFrame(columns=column_order)
    for col in column_order:
        if col in df.columns:
            df_ordered[col] = df[col]
        else:
            df_ordered[col] = ''

    # Save to TSV
    output_path = os.path.join(os.path.dirname(__file__), 'publications.tsv')
    df_ordered.to_csv(output_path, sep='\t', index=False)
    print(f"Successfully created {output_path}")

if __name__ == '__main__':
    main()
