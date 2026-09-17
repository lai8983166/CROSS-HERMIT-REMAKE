
void __fastcall FUN__text__0041d0d0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _eh_vector_constructor_iterator_(param_1 + 2,0x278,2,FUN__text__0041d2e0,FUN__text__0041d3c0);
  *local_8 = 0;
  local_8 = (undefined4 *)0x41d123;
  FUN__text__0056ce80();
  return;
}

