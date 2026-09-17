
void __thiscall FUN__text__0044b8b0(uint param_1,undefined1 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined2 local_10;
  undefined2 local_c;
  uint local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = 0;
  *(undefined4 *)(param_1 + 0x94) = 0;
  *(undefined1 *)(param_1 + 0x9f) = param_2;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  local_8 = param_1;
  FUN__text__0044cb40(param_1 + 0x38,param_1 & 0xffff0000,param_1 & 0xffff0000,0x5a,5,&DAT_006065d8)
  ;
  local_8 = 0x44b93f;
  FUN__text__0056ce80();
  return;
}

