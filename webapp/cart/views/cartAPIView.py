# cart는 설문 작성자가 사용하는 개념

# get all : db 상 저장되어 있는 모든 템플릿 객체 가져오기
# get all : db 상 저장되어 있는 모든 카트 객체 가져오기
# get detail : db 상 저장되어 있는 특정 템플릿 객체 가져오기 -> 템플릿 상세 조회 API 호출
# post : 특정 템플릿 객체를 카트에 담기
# update : 카트에 담았던 템플릿 객체를 수정하기
# delete : 카트에 담았던 모든 템플릿 객체를 삭제하기

# Cart Model
# survey : 어떤 설문조사에 대한 카트
# template : template 객체
# quantiy : template 객체의 개수

class Cart:
    pass