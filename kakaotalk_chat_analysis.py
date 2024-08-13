import re
from collections import defaultdict, Counter
from datetime import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

def parse_chat_data(file_path):
    chat_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'\[(.+?)\] \[(.+?)\] (.+)', line.strip())
            if match:
                nickname, time, message = match.groups()
                chat_data.append((nickname, time, message))
    return chat_data

def analyze_chat_times(chat_data, target_nickname):
    hour_counts = defaultdict(int)
    for nickname, time, _ in chat_data:
        if nickname == target_nickname:
            hour = datetime.strptime(time, '오전 %I:%M').hour if '오전' in time else \
                   (datetime.strptime(time, '오후 %I:%M').hour + 12) % 24
            hour_counts[hour] += 1
    return hour_counts

def visualize_chat_times(hour_counts, nickname):
    hours = range(24)
    counts = [hour_counts[hour] for hour in hours]
    
    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts)
    plt.title(f'{nickname}의 채팅 시간대 분포')
    plt.xlabel('시간')
    plt.ylabel('채팅 빈도')
    plt.xticks(hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def analyze_chat_ranking(chat_data):
    message_counts = Counter(nickname for nickname, _, _ in chat_data)
    return message_counts.most_common()

def visualize_chat_ranking(ranking):
    nicknames, counts = zip(*ranking)
    
    plt.figure(figsize=(12, 6))
    plt.bar(nicknames, counts)
    plt.title('채팅 참여자 순위')
    plt.xlabel('닉네임')
    plt.ylabel('메시지 수')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main():
    file_path = 'kakaotalk_chat_log.txt'  # 채팅 로그 파일 경로
    chat_data = parse_chat_data(file_path)

    # 시간대별 분석
    nickname = input("분석할 사용자의 닉네임을 입력하세요: ")
    if nickname:
        hour_counts = analyze_chat_times(chat_data, nickname)
        visualize_chat_times(hour_counts, nickname)
    else:
        # 채팅 순위 분석
        ranking = analyze_chat_ranking(chat_data)[:20]
        visualize_chat_ranking(ranking)

if __name__ == "__main__":
    main()