
void __fastcall FUN__text__00414090(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0xb210) != 0) {
    local_8 = param_1;
    _memset((void *)(param_1 + 0xb3e8),0,0x20);
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x40))
              (*(undefined4 *)(local_8 + 0xb210),0,0,&local_10);
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      (**(code **)(*local_10 + 0x20))(local_10,local_8 + 0xb3e8);
      local_c = FUN__text__0056ce80();
      if (-1 < local_c) {
        (**(code **)(*local_10 + 8))(local_10);
        FUN__text__0056ce80();
        *(undefined4 *)(local_8 + 0xb234) = *(undefined4 *)(local_8 + 0xb400);
        *(undefined4 *)(local_8 + 0xb238) = *(undefined4 *)(local_8 + 0xb404);
      }
    }
  }
  local_8 = 0x414188;
  FUN__text__0056ce80();
  return;
}

