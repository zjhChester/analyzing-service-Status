package com.analysis.testcollections.consumer;
import com.analysis.testcollections.TCollections;

@Service
@RequiredArgsConstructor
class CollectionsConsumer{
    private final TCollections tCollections;
    private void useList(){
        AdminRepository.errors.add("2");
        tCollections.getList().removeAll();
        tCollections.getList().remve();
        tCollections.getList().add("1");
        tCollections.getAccessObject().setXXX();
        TestCollections.accessObject1().setXXX();
        testCollections.accessObject1().setXXX();
    }
}