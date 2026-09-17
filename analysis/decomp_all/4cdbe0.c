
void __fastcall FUN__text__004cdbe0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005906a4;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  local_14 = param_1;
  _eh_vector_constructor_iterator_
            ((void *)(param_1 + 0x1ce),0x12,5,FUN__text__004c6d00,FUN__text__004c6d40);
  local_8 = 0;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x228),0x1a,0x14,FUN__text__004cb750,FUN__text__004cb790);
  local_8._0_1_ = 1;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x430),0xab8,10,FUN__text__004caa70,FUN__text__004cab80);
  local_8._0_1_ = 2;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x6f60),0xe0,10,FUN__text__004c9460,FUN__text__004c94e0);
  local_8._0_1_ = 3;
  FUN__text__004c7b90();
  local_8._0_1_ = 4;
  FUN__text__004c8f00();
  local_8 = CONCAT31(local_8._1_3_,5);
  FUN__text__004c7650();
  ExceptionList = local_10;
  local_8 = 0x4cdcf0;
  FUN__text__0056ce80();
  return;
}

