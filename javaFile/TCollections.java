package com.analysis.testcollections;

import com.ysg.productservice.common.general.exceptionhandling.BaseErrorCode;
import com.ysg.productservice.common.general.exceptionhandling.exception.AppException;
import com.ysg.productservice.common.specific.PriceType;
import lombok.Builder;
import lombok.Data;
import org.apache.commons.collections4.CollectionUtils;

import javax.validation.Valid;
import javax.validation.constraints.DecimalMax;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.Digits;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.math.BigDecimal;
import java.util.List;
import java.util.Objects;

@Data
@Builder
@Repository
public class TCollections {
    private final List<String> list = new ArrayList<>();
    private final AccessObject accessObject;
    public final AccessObject accessObject1;
    private Object testObject;
}
