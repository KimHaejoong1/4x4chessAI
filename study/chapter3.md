# Chapter 03 벨만 방정식

## 3.1 벨만 기대 방정식

### 0단계

$$
<img src="image/3-1.png">
$$

### 1단계

$$
v_{\pi}(s) = \sum_{a \in \mathcal{A}} \pi(a|s) q_{\pi}(s, a)
$$

$$
q_{\pi}(s, a) = r_{s}^{a} + \gamma \sum_{s' \in \mathcal{S}} p_{ss'}^{a} v_{\pi}(s')
$$

### 2단계

$$
v_{\pi}(s) = \sum_{a \in \mathcal{A}} \pi(a|s) \left( r_{s}^{a} + \gamma \sum_{s' \in \mathcal{S}} p_{ss'}^{a} v_{\pi}(s') \right)
$$

$$
q_{\pi}(s, a) = r_{s}^{a} + \gamma \sum_{s' \in \mathcal{S}} p_{ss'}^{a} \sum_{a' \in \mathcal{A}} \pi(a'|s') q_{\pi}(s', a')
$$

**모델-프리 접근법** : MDP에 대한 정보를 모를 때 학습하는 접근법

**모델 기반** or **플래닝** : 보상 함수와 전이 확률 분포를 알 때 학습하는 접근법

## 3.2 벨만 최적 방정식

### 최적 밸류와 최적 정책

**최적 밸류(optimal value)**에 대한 함수: $v_{\*}(s)$ 와 $q_{\*}(s, a)$


$$
v_{*}(s) = \max_{\pi} v_{\pi}(s)
$$

$$
q_{*}(s, a) = \max_{\pi} q_{\pi}(s, a)
$$

**최적 정책(optimal policy)** : 각 상태에서 최적 밸류를 갖게 하는 정책 $π_\*$

**부분 순서(partial ordering)** : 각 상태 구간 별 “더 좋다”에 대한 정의

→ 어쨋든  $π_\*$ 는 무조건 존재하므로 찾는 데 집중!

### 벨만 최적 방정식

벨만 기대 방정식의 확률적 요소 $\pi$ → $max$ 로 전환해주어 벨만 최적 방정식 도출
