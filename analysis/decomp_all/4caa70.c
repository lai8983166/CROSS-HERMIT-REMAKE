
void __fastcall FUN__text__004caa70(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005905c9;
  local_10 = ExceptionList;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  local_14 = param_1;
  _eh_vector_constructor_iterator_
            ((void *)(param_1 + 0x18),0x110,10,FUN__text__004cab00,FUN__text__004cab40);
  local_8 = 0;
  *(undefined2 *)(local_14 + 0x16) = 0;
  FUN__text__004cb0d0(10,0x14);
  ExceptionList = local_10;
  local_8 = 0x4caafc;
  FUN__text__0056ce80();
  return;
}

