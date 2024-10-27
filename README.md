# LoreKraft: The Future of MMORPGs
> **An AI-driven MMORPG engine with AI Dungeon Masters creating endless adventures.**


![image](https://github.com/user-attachments/assets/35e6f7d7-b5a7-4eab-84fe-7db6f5a8935f)

---

## Motivation
What happens when broke grad students, fueled by a passion for AI and late-night RPG marathons, dream big? You get **LoreKraft**—an AI-powered MMORPG engine where AI Dungeon Masters collaborate to generate dynamic and engaging worlds in real-time. With Generative AI, multi-agent systems, and our love for gaming, we set out to revolutionize RPGs into something more immersive, unpredictable, and intelligent.


---

## What We Learned
In Berkeley’s hackathon culture, we learned why we’d rather spend our weekends hacking than snacking! We dove into multi-agent systems, understanding how to create harmony among AI agents and push the limits of AI collaboration. Our efforts in combining creative text generation, efficient data handling, and game mechanics led us to a groundbreaking RPG experience powered by multi-agent AI.


---

## How We Built It

LoreKraft is built on a foundation of **multi-agent collaboration** where each agent has a specific role in the game’s ecosystem. Here’s a technical breakdown:

1. **Creative Text Generation**  
   Using **Gemini AI**, we generated immersive narratives to keep players engaged. Our AI Dungeon Master spun tales without tiring, adding endless creative twists to the gameplay.

2. **GPT Function Calls for Database Management**  
   With GPT-4’s function calling, we handled database queries and knowledge retrieval, tracking player stats and game dynamics seamlessly.

3. **Retrieval-Augmented Generation (RAG)**  
   We used RAG models to retrieve knowledge from our databases, ensuring that player attributes, inventory, and history were instantly accessible to AI agents.

![image](https://github.com/user-attachments/assets/00ce1047-8a8c-4b16-a2c1-76283791991b)

4. **Union of Experts (Agent-Based Collaboration)**  
   Each agent specialized in a task—whether map generation, combat events, or managing delayed events. Together, they collaborated like a council of Dungeon Masters, enhancing player experience.

5. **Frontend with Reflex AI**  
   We leveraged Reflex AI for a dynamic, interactive interface, allowing players to see the AI’s decisions reflected on the game board in real-time.

6. **Node.js for Session Management**  
   With **Node.js**, we maintained player sessions, supporting multiplayer interactions and state persistence.

7. **Backend with Flask**  
   **Flask** facilitated smooth communication between AI agents and the frontend, ensuring fast and reliable performance.

8. **Database Management**  
   A hybrid approach with **SingleStoreDB** for quick retrieval and **MongoDB** for handling unstructured data like character traits.

9. **Augmented Reality with Snap Spectacles**  
   For immersive gameplay, we integrated **Snap Spectacles** to bring the game world to life, blending virtual and real environments.


---

## Challenges We Faced

1. **Multi-Agent Orchestration**  
   Synchronizing multiple agents was a challenge, ensuring consistent responses without overwhelming the system.

2. **Data Optimization**  
   Efficient data handling between agents and databases was essential, prompting us to optimize retrieval and storage using hybrid databases.

3. **Beta Instability**  
   Working with cutting-edge AI tools in beta stages sometimes introduced instability, requiring us to adapt our approach for reliability.

4. **Session Handling at Scale**  
   Ensuring smooth transitions between game states and persistent sessions for multiple players was complex but rewarding.


---
## Implementation
![image](https://github.com/user-attachments/assets/1390c700-ac4b-4a63-9f4c-ba52695f3e4c)
![image](https://github.com/user-attachments/assets/17759a29-57ee-4786-92de-2001e597660b)
![image](https://github.com/user-attachments/assets/ad89b160-1a4e-4eba-95fe-d80b9313eca1)
---

## Final Thoughts
LoreKraft isn’t just a game engine; it’s a revolutionary approach to MMORPGs. Using multi-agent systems, we’re creating a world where multiple AI agents collaborate to build, manage, and evolve a game world based on player decisions. This kind of intelligent orchestration can offer unparalleled immersion and adaptability, crafting unique adventures for every player.


---

## Built With
- **fetchai**
- **flask**
- **gemini**
- **gpt**
- **hume**
- **javascript**
- **python**
- **reflex**
- **ripple**
- **singlestore**
- **snapchat**
- **vapi**

---

## Acknowledgments
Special thanks to the Berkeley Hackathon team and our mentors for their guidance and support throughout this project.

---

> Ready to experience the next level of MMORPGs? Join us in the adventure with LoreKraft!

---

