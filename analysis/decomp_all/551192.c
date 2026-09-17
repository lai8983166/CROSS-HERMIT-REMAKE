
void FUN__text__00551192(int param_1)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  puVar1 = (undefined4 *)(*(code *)**(undefined4 **)(param_1 + 4))(param_1,1,0x30);
  *(undefined4 **)(param_1 + 0x19c) = puVar1;
  *(undefined1 *)(puVar1 + 2) = 0;
  *puVar1 = &LAB__text__00550d6a;
  puVar1[10] = *(int *)(param_1 + 100) * *(int *)(param_1 + 0x5c);
  if (*(int *)(param_1 + 0x110) == 2) {
    puVar1[1] = FUN__text__00550d7f;
    puVar1[3] = FUN__text__00550fac;
    uVar2 = (**(code **)(*(int *)(param_1 + 4) + 4))(param_1,1,puVar1[10]);
    puVar1[8] = uVar2;
  }
  else {
    puVar1[8] = 0;
    puVar1[1] = FUN__text__00550e25;
    puVar1[3] = FUN__text__00550e56;
  }
  FUN__text__00550cba();
  return;
}

