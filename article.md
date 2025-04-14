# AI for Animal Care

## Introduction

The era of large language models (LLMs) began in 2017 with the publication of *"Attention Is All You Need"* by Vaswani et al. [[1]](https://arxiv.org/abs/1706.03762). This groundbreaking paper introduced the transformer architecture, laying the foundation for a revolution in how machines process and generate human language. Since then, LLMs have rapidly evolved, powering applications that range from conversational agents to code generation and medical question answering.

Yet, despite their remarkable capabilities, LLMs are still underutilized across many sectors. Industry adoption often lags behind research advancements, and public awareness of their true potential remains limited. However, the landscape is changing fast — particularly as LLMs are increasingly integrated into intelligent agents, opening up transformative real-world applications.

One such opportunity was the **5-Day Generative AI Workshop** hosted by **Kaggle and Google**, which introduced participants to modern generative AI techniques. As part of the capstone project, I chose to build a **veterinary assistant chatbot**, powered by *Retrieval-Augmented Generation (RAG)* and grounded in authoritative content from the **Merck Veterinary Manual**.

---

## Why Veterinary Science?

Veterinary medicine — particularly in low-resource and rural regions — remains one of the fields where LLMs can make a significant impact. Access to up-to-date veterinary knowledge is often limited, and qualified professionals may be scarce. Animal welfare suffers as a result, with growing street dog populations, preventable diseases, and misinformation contributing to systemic challenges.

A well-designed, AI-powered assistant that provides **reliable, verifiable, and scientifically grounded veterinary information** could empower animal caretakers, improve outcomes, and support broader public health efforts.

---

## What This Project Covers

This project outlines the development of a veterinary chatbot that:

- Answers user queries using *retrieved context* from vetted Merck Veterinary articles  
- Generates natural and informative responses with source citations  
- Demonstrates key Gen AI capabilities such as **RAG**, **document understanding**, and **structured output**

Later sections will explore implementation steps, showcase example interactions, and suggest future enhancements, such as multimodal input or integration with diagnostic tools.

## Web Scraping

The first challenge in building a chatbot that is providing scientifically grounded responses based on **RAG** is to retrieve content from an authoritative source. The **Merck Veterinary Manual** provides such a source. However, they dont provide an **API**, so that retrieval of their webcontent needs to happen manually. 
This was actually one of the biggest parts of the project and a very interesting one as well. 
I decided to use *Playwright*, a more modern alternative to *Selenium* that allows webscraping even if the website to scrape uses JavaScript to dynamically generate and retrieve content. 
In hindsight, just using *BeautifulSoup* would have been enough, as it turns out that [https://www.merckvetmanual.com/] does not implement dynamic content loading. 

## Web Scraping

The first challenge in building a **chatbot powered by Retrieval-Augmented Generation (RAG)** is sourcing reliable and authoritative content. For this project, I chose the **Merck Veterinary Manual**—a well-respected and freely accessible resource in the field of veterinary science.
As Merck does not offer a public **API**, the only way to retrieve their content was by scraping it directly from the website. This turned out to be one of the more time-consuming and at the same time technically interesting parts of the project.

I decided to implement the Web Scraping with python and the **Playwright** package, a modern alternative to **Selenium** that is particularly useful when scraping websites that load their content dynamically via JavaScript. Playwright allows for automated interaction with the browser, enabling robust scraping even from complex web applications.

In hindsight, however, the Merck website does **not** rely on JavaScript for dynamic content loading—meaning a much simpler approach using tools like **BeautifulSoup** would have been enough. Still, this detour provided valuable experience and flexibility for scraping more complex websites in the future.

