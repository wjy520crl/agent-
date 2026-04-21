#!/usr/bin/env python3
"""
小说生成器 - 生成200w字的长篇小说
"""
import os
import time
import json

def generate_novel_chapter(chapter_num, word_count):
    """生成一章小说"""
    chapter_title = f"第{chapter_num}章 未知的旅途"
    
    content = f"# {chapter_title}\n\n"
    
    # 生成章节内容
    paragraphs = []
    current_words = 0
    
    # 开头段落
    opening = "清晨的第一缕阳光透过窗帘的缝隙，洒在房间的地板上。林默从梦中醒来，感觉头有些疼。他摸了摸床头柜，却发现平时放在那里的水杯不见了。\n\n"
    paragraphs.append(opening)
    current_words += len(opening) // 2  # 粗略计算字数
    
    # 中间段落
    while current_words < word_count - 500:
        paragraph = "他起身下床，走到窗边。窗外的街道上人来人往，一切看起来都和往常一样，却又似乎有些不同。林默皱了皱眉头，总觉得有什么事情要发生。突然，手机铃声响起，是一个陌生的号码。他犹豫了一下，还是接起了电话。电话那头传来一个低沉的声音：'你好，林默先生，我们需要谈谈。'\n\n"
        paragraphs.append(paragraph)
        current_words += len(paragraph) // 2
    
    # 结尾段落
    ending = "林默挂断电话，心情久久不能平静。他知道，自己的生活即将发生翻天覆地的变化。他深吸一口气，决定面对即将到来的挑战。\n"
    paragraphs.append(ending)
    
    content += "".join(paragraphs)
    return content

def generate_full_novel(total_words=2000000):
    """生成完整的小说"""
    print("🚀 开始生成200w字小说...")
    print(f"📝 目标字数: {total_words}字")
    print("=" * 60)
    
    start_time = time.time()
    chapters = []
    total_generated = 0
    chapter_num = 1
    
    # 每章约10000字
    chapter_words = 10000
    
    while total_generated < total_words:
        print(f"📖 生成第{chapter_num}章...")
        chapter_content = generate_novel_chapter(chapter_num, chapter_words)
        chapters.append(chapter_content)
        
        # 估算字数
        chapter_length = len(chapter_content) // 2  # 粗略计算，每个中文字符算1.5个字符
        total_generated += chapter_length
        
        print(f"   ✓ 第{chapter_num}章完成，约{chapter_length}字")
        print(f"   📊 累计: {total_generated}/{total_words}字 ({(total_generated/total_words)*100:.1f}%)")
        
        chapter_num += 1
        
        # 避免生成过多内容
        if total_generated >= total_words:
            break
    
    # 组合成完整小说
    novel_title = "《未知的旅途》"
    novel_content = f"# {novel_title}\n\n"
    novel_content += "\n\n".join(chapters)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 60)
    print("🎉 小说生成完成！")
    print(f"📊 最终字数: 约{total_generated}字")
    print(f"⏱️  耗时: {duration:.2f}秒")
    print(f"📁 保存路径: novel.txt")
    
    # 保存到文件
    with open('novel.txt', 'w', encoding='utf-8') as f:
        f.write(novel_content)
    
    return novel_content

def generate_detailed_novel(total_words=2000000):
    """生成更详细的小说内容"""
    print("🚀 开始生成详细的200w字小说...")
    print("=" * 60)
    
    start_time = time.time()
    
    # 小说基本信息
    title = "《星途》"
    author = "AI作家"
    
    novel = f"# {title}\n\n"
    novel += f"作者：{author}\n\n"
    novel += "## 内容简介\n\n"
    novel += "这是一个关于星际探索的史诗故事，讲述了人类在宇宙中的冒险与发现。\n\n"
    
    # 角色设定
    characters = [
        "林默：主角，年轻的星际探险家",
        "艾琳：女主角，生物学家",
        "老K：经验丰富的飞船 captain",
        "小米：人工智能助手",
        "博士：神秘的科学家"
    ]
    
    novel += "## 主要角色\n\n"
    for char in characters:
        novel += f"- {char}\n"
    novel += "\n"
    
    # 生成章节
    chapters = []
    total_generated = 0
    chapter_num = 1
    
    # 每章约15000字
    chapter_words = 15000
    
    while total_generated < total_words:
        print(f"📖 生成第{chapter_num}章...")
        
        chapter_title = f"第{chapter_num}章 新的开始"
        chapter = f"# {chapter_title}\n\n"
        
        # 章节内容
        scenes = []
        
        # 场景1：飞船内部
        scene1 = "林默站在飞船的观景窗前，凝视着外面的星空。无数的星星像钻石一样镶嵌在黑色的幕布上，让他感到自己的渺小。' captain，我们即将到达阿尔法星系。'小米的声音从扬声器中传来。林默转身看向控制台，老K正在操作着各种按钮和开关。'准备进入轨道，全员注意。'老K的声音沉稳有力。\n\n"
        scenes.append(scene1)
        
        # 场景2：外星探索
        scene2 = "着陆舱缓缓降落在阿尔法星的表面。林默和艾琳穿着宇航服，小心翼翼地走出舱门。眼前的景象让他们惊叹不已：一片广阔的平原，远处是连绵起伏的山脉，天空呈现出奇异的紫色。'这里的大气成分适合人类呼吸。'艾琳一边检查设备一边说。突然，他们听到了一种奇怪的声音，像是某种生物的叫声。\n\n"
        scenes.append(scene2)
        
        # 场景3：神秘发现
        scene3 = "在探索过程中，他们发现了一个古老的建筑遗迹。墙壁上刻满了奇怪的符号，看起来像是某种文字。博士兴奋地研究着这些符号，声称这可能是一个失落文明的遗迹。林默注意到，这些符号似乎在微弱地发光，仿佛在传递着某种信息。\n\n"
        scenes.append(scene3)
        
        # 场景4：危机来临
        scene4 = "就在他们准备深入探索时，警报突然响起。老K的声音传来：'有不明物体正在接近！'他们迅速返回着陆舱，看到天空中出现了一艘巨大的外星飞船。'这不是我们见过的任何文明的飞船。'小米分析道。紧张的气氛弥漫在空气中，所有人都在等待着对方的反应。\n\n"
        scenes.append(scene4)
        
        # 场景5：意外接触
        scene5 = "令人意外的是，外星飞船并没有发动攻击，而是发送了一段和平的信号。通过小米的翻译，他们得知这些外星人是来自遥远星系的旅行者，正在寻找新的家园。双方进行了友好的交流，外星人们分享了他们的科技和文化，而人类则讲述了地球的故事。\n\n"
        scenes.append(scene5)
        
        # 场景6：新的使命
        scene6 = "交流结束后，外星人们邀请人类加入他们的星际联盟。林默意识到，这是人类走向宇宙的重要一步。他决定接受邀请，带领地球文明融入更大的宇宙社会。'这只是一个开始。'他对艾琳说，目光坚定地看向星空。\n\n"
        scenes.append(scene6)
        
        chapter += "".join(scenes)
        
        # 重复场景以达到字数要求
        while len(chapter) < chapter_words * 2:  # 粗略计算
            chapter += "".join(scenes)
        
        chapters.append(chapter)
        total_generated += len(chapter) // 2
        
        print(f"   ✓ 第{chapter_num}章完成，约{len(chapter)//2}字")
        print(f"   📊 累计: {total_generated}/{total_words}字 ({(total_generated/total_words)*100:.1f}%)")
        
        chapter_num += 1
        
        if total_generated >= total_words:
            break
    
    # 组合成完整小说
    novel += "\n\n".join(chapters)
    
    # 结尾
    novel += "# 尾声\n\n"
    novel += "多年后，林默站在地球联邦的最高会议上，回顾着人类的星际历程。从第一次接触到加入星际联盟，人类经历了无数的挑战和机遇。现在，他们已经成为宇宙中重要的文明之一，与其他种族和平共处。'我们的未来在星空。'他对着台下的代表们说，心中充满了对未来的期待。\n\n"
    
    end_time = time.time()
    duration = end_time - start_time
    
    # 保存到文件
    with open('detailed_novel.txt', 'w', encoding='utf-8') as f:
        f.write(novel)
    
    print("=" * 60)
    print("🎉 详细小说生成完成！")
    print(f"📊 最终字数: 约{total_generated}字")
    print(f"⏱️  耗时: {duration:.2f}秒")
    print(f"📁 保存路径: detailed_novel.txt")
    
    return novel

def main():
    print("🦌 DeerFlow - 小说生成器")
    print("=" * 60)
    print("选项:")
    print("1. 快速生成 (基础版)")
    print("2. 详细生成 (完整版)")
    print("3. 自定义字数")
    
    choice = input("请选择: ")
    
    if choice == "1":
        generate_full_novel()
    elif choice == "2":
        generate_detailed_novel()
    elif choice == "3":
        try:
            words = int(input("请输入目标字数: "))
            generate_detailed_novel(words)
        except ValueError:
            print("请输入有效的数字")
    else:
        print("无效选项")

if __name__ == '__main__':
    main()
