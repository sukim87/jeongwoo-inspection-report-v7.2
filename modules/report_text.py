import re

# Frequent field-entry typos and spacing. The draft always shows the corrected text before Excel creation.
REPLACEMENTS={
 '외관상태양호':'외관 상태 양호','외관상태 양호':'외관 상태 양호','이상없슴':'이상 없음','이상 업음':'이상 없음',
 '기준미달':'기준 미달','스팩':'스펙','스펙미달':'스펙 미달','도막두게':'도막두께','도막 두게':'도막두께',
 '치수이상없음':'치수 이상 없음','누설없음':'누설 없음','변형없음':'변형 없음','부식없음':'부식 없음',
 '재도장실시':'재도장 실시','재검사실시':'재검사 실시','사진참조':'사진 참조','도면참조':'도면 참조',
 '합격으로판정':'합격으로 판정','불합격으로판정':'불합격으로 판정'
}

def correct_text(text):
 text=(text or '').strip()
 for a,b in REPLACEMENTS.items(): text=text.replace(a,b)
 text=re.sub(r'\s+',' ',text)
 text=re.sub(r'\s*([,;/])\s*',r'\1 ',text)
 return text.strip()

def make_draft(types,spec,inspection_result,judgment,count,inspection_location=''):
 title=' / '.join(types) if types else '검사'
 spec=correct_text(spec); inspection_result=correct_text(inspection_result)
 if judgment=='합격':
  result=f"{title} 결과, {inspection_result}로 확인되었으며 적용 기준({spec})을 충족하여 합격으로 판정함."
  action='별도 조치사항 없음.'
 elif judgment=='불합격':
  result=f"{title} 결과, {inspection_result}로 확인되었으며 적용 기준({spec})을 충족하지 못하여 불합격으로 판정함."
  action='부적합 부위를 수정·보수한 후 동일 기준으로 재검사하고 결과를 확인할 것.'
 elif judgment=='조건부 합격':
  result=f"{title} 결과, {inspection_result}로 확인되었으며 지정된 보완조건 이행을 전제로 조건부 합격으로 판정함."
  action='지정된 보완사항을 완료하고 객관적 증빙을 확인한 후 최종 승인할 것.'
 else:
  result=f'{title} 항목은 해당 없음(N/A)으로 처리함.'; action='해당 없음.'
 caption=f"사진 1~{count}: {title} 대상 및 검사 상태" if count else ''
 if inspection_location:
  result += f" 검사장소: {correct_text(inspection_location)}."
 return result,action,caption,spec,inspection_result
