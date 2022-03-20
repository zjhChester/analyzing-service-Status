package com.analysis.testcollections.consumer;
import com.analysis.testcollections.TestCollections;

@Service
@RequiredArgsConstructor
class CollectionsConsumer{
    private final TestCollections testCollections;
    private void useList(){
        AdminRepository.errors.add("2");
        testCollections.getList().removeAll();
        testCollections.getList().remve();
        testCollections.getList().add("1");
    }
}