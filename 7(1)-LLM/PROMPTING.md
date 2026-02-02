# 🎯 Prompting Strategy report

본 보고서는 Direct Prompting, Chain-of-Thought Prompting, 그리고 직접 설계한 My Prompting 전략을 0-shot, 3-shot, 5-shot 조건에서 비교하여 각 프롬프트 기법의 성능 차이와 그 원인을 분석한다.

## 1. Prompting Strategy별 정답률 비교

| Prompting Method | 0-shot | 3-shot | 5-shot |
|------------------|--------|--------|--------|
| Direct Prompting | 0.78   | 0.68   | 0.80   |
| CoT Prompting    | 0.82   | 0.84   | 0.80   |
| My Prompting     | 0.84   | 0.88   | 0.80   |

표를 통해 확인할 수 있듯이, prompting 전략에 따라 few-shot 예제 증가에 대한 반응이 다르게 나타난다.

Direct Prompting의 경우 3-shot에서 오히려 성능이 하락하는 현상을 보였는데 이는 예제가 추가되었음에도 불구하고 명시적인 추론 지시가 없어 모델이 예제를 효과적으로 일반화하지 못했기 때문으로 해석할 수 있다.

반면 CoT Prompting과 My Prompting은 few-shot 환경에서 비교적 안정적인 성능을 유지하며 특히 구조화된 추론을 요구하는 프롬프트가 예제의 도움을 더 잘 활용함을 보여준다.

한편 5-shot 환경에서는 모든 prompting 전략에서 성능 향상이 제한적으로 나타났다. 이는 GSM8K 문제의 특성상 일정 수준 이상의 예제가 제공되면 추가 예제가 더 이상 큰 정보를 제공하지 못하고 오히려 입력 길이 증가로 인해 효율이 감소할 수 있음을 시사한다.

## 2. CoT Prompting이 Direct Prompting보다 효과적인 이유

Direct Prompting은 모델이 문제를 보고 곧바로 정답을 출력하도록 유도하는 방식이다. 이 방식은 간단한 문제에서는 효율적일 수 있지만, 여러 단계의 계산이나 조건 해석이 필요한 문제에서는 중간 추론 과정이 생략되어 계산 실수나 논리적 오류가 발생할 가능성이 높다.

반면, CoT Prompting은 문제를 단계별로 reasoning하도록 유도함으로써 모델이 문제의 조건을 명확히 파악하고 중간 계산을 체계적으로 수행할 수 있게 한다.

이로 인해 복합적인 수학 문제에서 정답률이 향상될 수 있으며 실험 결과에서도 CoT Prompting은 Direct Prompting보다 전반적으로 더 높은 성능을 보였다.

## 3. My Prompting이 CoT Prompting보다 효과적인 이유

직접 설계한 My Prompting은 CoT Prompting의 "단계적 추론 유도"라는 장점을 유지하면서 추가적으로 **출력 형식의 일관성**과 **평가/파싱 안정성**을 강화하여 성능이 더 높아질 수 있도록 하였다.

My Prompting에서는 문제 해결 과정을 단계적으로 수행한 뒤 마지막 줄에 반드시 Answer: <number> 형식으로 정답을 출력하도록 명시적으로 지시하였다. 이러한 구조는 추론을 작성한 뒤 최종적으로 정답 라인을 완성하도록 유도하며 정답 추출 함수가 "Answer:" 패턴을 안정적으로 매칭할 수 있게 한다. 결과적으로 CoT Prompting에서 발생할 수 있는 정답 라인이 문장 속에 섞이거나 형식이 흔들리는 문제를 완화하여 정답 파싱 실패로 인한 오답 처리 가능성을 줄인다.

또한 GSM8K train 데이터셋에서 샘플링한 few-shot 예제를 활용하여 Question → Reasoning → Answer 흐름을 일관된 형식으로 제공함으로써 모델이 동일한 서술 구조를 따르도록 유도하였다. 특히 예제에는 데이터셋에 포함된 풀이(Reasoning)와 정답(Answer)을 함께 제시하여 모델이 계산 과정을 전개한 뒤 마지막에 정답 라인을 출력하는 패턴을 학습하도록 설계하였다.

마지막으로 temperature=0.0으로 고정하여 출력의 변동성을 줄이고 실험의 재현성을 높였다. 이를 통해 self-consistency처럼 다중 샘플링을 사용하지 않더라도 동일 조건에서 비교적 안정적인 성능 측정이 가능하도록 하였다.