
void __fastcall FUN__text__004c7be0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _eh_vector_constructor_iterator_
            ((void *)(param_1 + 0x18),0x80,5,FUN__text__004075e0,FUN__text__00407710);
  local_8 = 0x4c7c2a;
  FUN__text__0056ce80();
  return;
}

